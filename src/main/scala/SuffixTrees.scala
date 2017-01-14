import scala.collection.mutable.{HashMap}

/**
  * Created by horus on 1/10/2017.
  */

object Util {
  implicit class StringHelper(string: String) {
    def lastIndex: Int = string.length() - 1
  }

  case class Range(start: Int, end: Int) {
    def length = end - start + 1
  }
}

object SuffixTrees {
  import Util._

  // stateful stuff
  class Node {
    val outEdges = HashMap.empty[Char, Edge]
    var suffixEdge: Option[SuffixEdge] = None

    def nextNode(default: Node) = suffixEdge   .map( _.targetNode ) .getOrElse(default)
  }

  class SuffixEdge(val targetNode: Node)

  class Edge(var startIndex: Int) {
    var extent: EdgeExtent = Leaf
  }

  sealed trait EdgeExtent
  case object Leaf extends EdgeExtent
  case class Internal(length: Int, targetNode: Node) extends EdgeExtent {
  }

  // immutables

  // algorithm types
  case class AlgorithmProgress(index: Int, currentSuffix: Int) {
    def suffixRange = Range(index - currentSuffix + 1, index)
    // def view(string: String): StringView
  }

  object AlgorithmProgress {
    val start = AlgorithmProgress(-1, 0)
  }

  sealed trait Cursor
  case class NodeCursor(baseNode: Node) extends Cursor
  case class EdgeCursor(baseNode: Node, edgePos: EdgePosition) extends Cursor
  case class EdgePosition(activeEdge: Char, activeLength: Int)

  def suffixTree(string: String): Node = {
    val root = new Node
    makeSuffixTree(string, AlgorithmProgress.start, root, NodeCursor(root), None)
  }

  def splitEdge(edge: Edge, activeLength: Int,
                newIndex: Int,
                prefixNode: Option[Node],
                string: String)
  : Node = {

    val newNode = new Node
    val newEdge = new Edge(newIndex)

    // algorithm is incorrect without this line!
    // oldNode.suffixEdge = Some(new SuffixEdge(newNode))

    val lowerStartIndex = edge.startIndex + activeLength

    // edge gets shortened
    var upperEdge = edge // just an alias
    val lowerEdge = new Edge(lowerStartIndex)

    lowerEdge.extent = edge.extent match {
      case Leaf => Leaf
      case Internal(edgeLength, targetNode) => Internal(edgeLength - activeLength, targetNode)
    }
    upperEdge.extent = Internal(activeLength, newNode)

    val splitChar = string(lowerStartIndex)
    newNode.outEdges.update(splitChar,lowerEdge)

    val insertChar = string(newIndex)
    newNode.outEdges.update(insertChar,newEdge)

    newNode
  }

  def makeSuffixTree(string: String, progress: AlgorithmProgress, root: Node, cursor: Cursor, prefixNode: Option[Node])
  : Node = {
    // are these lazy?

    progress match {

      // chamber another character?
      case AlgorithmProgress(index, 0) => {
        if (index + 1 >= string.length) root
        else makeSuffixTree(string, AlgorithmProgress(index + 1, 1), root, NodeCursor(root), None)
      }

      // do an operation on the graph?
      case AlgorithmProgress(index, currentSuffix) => {
        val insertChar = string(progress.suffixRange.end)

        cursor match {

          case NodeCursor(node) => {
            val edgeOption = node.outEdges.get(insertChar)
            edgeOption match {

              // insert a new edge
              case None => {
                val newEdge = new Edge(index)
                node.outEdges.update(insertChar, newEdge)

                val nextProgress = AlgorithmProgress(index, currentSuffix - 1)
                val nextNode = node.suffixEdge.map(_.targetNode).getOrElse(root)
                makeSuffixTree(string, nextProgress, root, NodeCursor(nextNode), None)
              }

              // queue the suffix and move on
              case Some(edge) => {
                val nextCursor = EdgeCursor(node, EdgePosition(insertChar, 1))
                val nextProgress = AlgorithmProgress(index + 1, currentSuffix + 1)
                makeSuffixTree(string, nextProgress, root, nextCursor, None)
              }
            }
          }

          case EdgeCursor(node, EdgePosition(rootChar, activeLength)) => {
            val edge = node.outEdges(rootChar) // it must exist, or the algorithm is incorrect!

            edge.extent match {

              case Leaf => {
                val newNode = splitEdge(edge, activeLength, index, prefixNode, string)

                // setup next iteration
                val nextNode = newNode.nextNode(root)
                val nextProgress = AlgorithmProgress(index, currentSuffix - 1)

                // compute next cursor
                val nextCursor = activeLength - 1 match {
                  case 0 => NodeCursor(nextNode)
                  case nextActiveLength => {
                    val nextSuffixHead = string(progress.suffixRange.start + 1)
                    EdgeCursor(nextNode, EdgePosition(nextSuffixHead, nextActiveLength))
                  }
                }

                makeSuffixTree(string, nextProgress, root, nextCursor, Some(node))
              }

              case Internal(edgeLength, targetNode) => {

                if (activeLength < edgeLength) {
                  val newNode = splitEdge(edge, activeLength, index, prefixNode, string)

                  // setup next iteration
                  val nextNode = newNode.nextNode(root)
                  // this can be shortcutted; pretty sure
                  val nextCursor = EdgeCursor(nextNode, EdgePosition(rootChar, activeLength - 1))
                  val nextProgress = AlgorithmProgress(index, currentSuffix - 1)

                  makeSuffixTree(string, nextProgress, root, nextCursor, Some(node))
                }

                else if (activeLength == edgeLength) {
                  makeSuffixTree(string, progress, root, NodeCursor(targetNode), prefixNode)
                }

                else {
                  val firstIndexAfterEdge = progress.suffixRange.start + edgeLength
                  val branchChar: Char = string(firstIndexAfterEdge)

                  val nextCursor = EdgeCursor(targetNode, EdgePosition(branchChar, activeLength - edgeLength))
                  makeSuffixTree(string, progress, root, nextCursor, prefixNode)
                }
              }
            }
          }
        }
      }
    }
  }

  def main(args: Array[String]): Unit = {
    println("Hello")

    println(suffixTree("Hello"))
  }
}
