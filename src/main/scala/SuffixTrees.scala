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
    val outEdges = HashMap.empty[Char, Edge];
    var suffixEdge: Option[SuffixEdge] = None;
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
    val start = AlgorithmProgress(0, 0)
  }

  sealed trait Cursor
  case class NodeCursor(baseNode: Node) extends Cursor
  case class EdgeCursor(baseNode: Node, edgePos: EdgePosition) extends Cursor
  case class EdgePosition(activeEdge: Char, activeLength: Int)

  def checkCursor(progress: AlgorithmProgress, string: String)(cursor: Cursor): Cursor = cursor match {
    // if the cursor is of edge type, and could shoot beyond the current edge, check it
    case EdgeCursor(node, EdgePosition(rootChar, activeLength)) => {
      val edge = node.outEdges(rootChar)

      edge.extent match {
        case Internal(edgeLength, targetNode) => {
          if (activeLength < edgeLength) {
            cursor
          }

          else if (activeLength == edgeLength) {
            NodeCursor(targetNode)
          }

          else {
            // suffix starts at progress.index - progress.currentbranch poi
            val firstIndexAfterEdge = progress.suffixRange.start + edgeLength
            val branchChar: Char = string(firstIndexAfterEdge)

            checkCursor(progress, string)(EdgeCursor(targetNode,EdgePosition(branchChar, activeLength-edgeLength)))
          }
        }

        case _ => cursor
      }
    }

    case _ => cursor
  }

  def makeSuffixTree(string: String, progress: AlgorithmProgress, root: Node, cursor: Cursor)
  : Node = {
    // are these lazy?
    val insertChar = string(progress.suffixRange.end)

    progress match {

      // chamber another character?
      case AlgorithmProgress(index, 0) => {
        if (index >= string.lastIndex) root
        else makeSuffixTree(string, AlgorithmProgress(index + 1, 1), root, NodeCursor(root))
      }

      // do an operation on the graph?
      case AlgorithmProgress(index, currentSuffix) => cursor match {

        case NodeCursor(node) => {
          val edgeOption = node.outEdges.get(insertChar)
          edgeOption match {

            // insert a new edge
            case None => {
              val newEdge = new Edge(index)
              node.outEdges.update(insertChar, newEdge)

              val nextProgress = AlgorithmProgress(index, currentSuffix - 1)
              val nextNode = node.suffixEdge   .map(_.targetNode)   .getOrElse(root)
              makeSuffixTree(string, nextProgress, root, NodeCursor(nextNode))
            }

            // queue the suffix and move on
            case Some(edge) => {
              val nextProgress = AlgorithmProgress(index+1, currentSuffix+1)
              val nextCursor = EdgeCursor(node, EdgePosition(insertChar,1))
              makeSuffixTree(string, nextProgress, root, nextCursor)
            }
          }
        }

        case EdgeCursor(node, EdgePosition(rootChar, activeLength)) => {}
      }

    }
  }

  def suffixTree(string: String): Node = {
    val root = new Node
    makeSuffixTree(string, AlgorithmProgress.start, root, NodeCursor(root))
  }

  def main(args: Array[String]): Unit = {
    println("Hello")

    println(suffixTree("Hello"))
  }
}
