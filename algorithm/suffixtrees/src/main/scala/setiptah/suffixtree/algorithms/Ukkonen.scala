/**
  * Created by ktreleav on 7/4/2017.
  */
package setiptah.suffixtree.algorithms

import setiptah.suffixtree.SuffixTrees._
import setiptah.util.StringUtil.Range

// Ukkonen's algorithm in scala, from http://stackoverflow.com/questions/9452701/ukkonens-suffix-tree-algorithm-in-plain-english

object UkkonenDriver extends SuffixTreeAlgorithmDriverAdapter(Ukkonen)


object Ukkonen extends SuffixTreeAlgorithm {

  def suffixTree(string: String): Node = {
    val root = new Node
    new SuffixTreeBuilder(root, string).makeSuffixTree(AlgorithmProgress.start, NodeCursor)(None, root)
  }

  // algorithm types
  case class AlgorithmProgress(
                                index: Int, // The last index of the prefix for which the tree being built is a suffix tree.
                                currentSuffix: Int  // The length of the last bit of the prefix that still needs some processing.
                              ) {
    def suffixRange = Range(index - currentSuffix + 1, index)
  }

  object AlgorithmProgress {
    val start = AlgorithmProgress(-1, 0)
  }

  sealed trait Cursor
  case object NodeCursor extends Cursor
  case class EdgeCursor(activeChar: Char, activeLength: Int) extends Cursor

  /** Splits an edge after activeLength characters to create a "tee".
    * One branch maintains the subtree of the original edge.
    * The other branch starts a subtree from position newIndex in string.
    * TODO(ktreleav): Manage suffix edges...
    * Returns the new terminal node of the new edge.
    */
  def splitEdge(activeLength: Int,
                newIndex: Int, string: String)(edge: Edge): Node = {

    val newNode = new Node
    val newEdge = new Edge(newIndex)

    // algorithm is incorrect without this line!
    // oldNode.suffixEdge = Some(new SuffixEdge(newNode))

    val lowerStartIndex = edge.startIndex + activeLength

    // edge gets shortened
    var upperEdge = edge // just an alias; edge is modified in place
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

  class SuffixTreeBuilder(root: Node, string: String) {
    def makeSuffixTree(progress: AlgorithmProgress, cursor: Cursor)(prefixNode: Option[Node], cursorNode: Node)
    : Node = {
      // are these lazy?

      progress match {

        // chamber another character?
        case AlgorithmProgress(index, 0) => {
          if (index + 1 >= string.length) root
          else makeSuffixTree(AlgorithmProgress(index + 1, 1), NodeCursor)(None, root)
        }

        // do an operation on the graph?
        case AlgorithmProgress(index, currentSuffix) => {
          val insertChar = string(progress.suffixRange.end)

          cursor match {

            case NodeCursor => {
              val edgeOption = cursorNode.outEdges.get(insertChar)
              edgeOption match {

                // insert a new edge
                case None => {
                  val newEdge = new Edge(index)
                  cursorNode.outEdges.update(insertChar, newEdge)

                  val nextProgress = AlgorithmProgress(index, currentSuffix - 1)
                  val nextNode = cursorNode.suffixEdge.map(_.targetNode).getOrElse(root)
                  makeSuffixTree(nextProgress, NodeCursor)(None, nextNode)
                }

                // queue the suffix and move on
                case Some(edge) => {
                  val nextCursor = EdgeCursor(insertChar, 1)
                  val nextProgress = AlgorithmProgress(index + 1, currentSuffix + 1)
                  makeSuffixTree(nextProgress, nextCursor)(None, cursorNode)
                }
              }
            }

            case EdgeCursor(rootChar, activeLength) => {
              val edge = cursorNode.outEdges(rootChar) // it must exist, or the algorithm is incorrect!

              def splitAction(): Node = {
                // do a split! does the newNode get used?
                val newNode = splitEdge(activeLength, index, string)(edge)
                // connect from any previously inserted node --- foreach for Option is "where not None"
                prefixNode.foreach( _.suffixEdge = Some(new SuffixEdge(newNode)) )

                // setup the next iteration
                val nextNode = cursorNode.nextNode(root) // is this always root?
                val nextProgress = AlgorithmProgress(index, currentSuffix - 1)

                // compute next cursor: root or non root?
                // this was the last remaining bug:
                // I just didn't remember from the "rules" that root and non-root have different behavior...
                // tests helped greatly here!
                val nextCursor = if ( cursorNode == root ) {
                  activeLength - 1 match {
                    case 0 => NodeCursor
                    case nextActiveLength => {
                      val nextSuffixHead = string(progress.suffixRange.start + 1)
                      EdgeCursor(nextSuffixHead, nextActiveLength)
                    }
                  }
                }
                else {
                  cursor
                }

                // Ukkonen says tail of suffix edge is the inserted node
                makeSuffixTree(nextProgress, nextCursor)(Some(newNode), nextNode)
              }

              def properEdgeAction(): Node = {
                val activeIndex = edge.startIndex + activeLength
                val activeChar = string(activeIndex)

                if (activeChar == insertChar) {
                  // kick the can down the road; e.g., don't propagate prefixNode
                  val nextProgress = AlgorithmProgress(index + 1, currentSuffix + 1)
                  val nextCursor = EdgeCursor(rootChar, activeLength + 1)
                  // TODO(ktreleav): optimize since I know it's a leaf from here on!
                  makeSuffixTree(nextProgress, nextCursor)(None, cursorNode)
                }

                else {
                  splitAction()
                }
              }

              edge.extent match {
                // any cursor on a leaf edge is a "proper" cursor
                case Leaf => {
                  properEdgeAction()
                }

                case Internal(edgeLength, targetNode) => {

                  if (activeLength < edgeLength) {
                    // a cursor whose activeLength is less than the edgeLength is also proper!
                    properEdgeAction()
                  }

                  else if (activeLength == edgeLength) {
                    // such cursor is actually pointing at the next node, isn't it...
                    makeSuffixTree(progress, NodeCursor)(prefixNode, targetNode)
                  }

                  else {
                    // cursor points beyond the target node; keep unwinding...
                    val firstIndexAfterEdge = progress.suffixRange.start + edgeLength
                    val branchChar: Char = string(firstIndexAfterEdge)

                    val nextCursor = EdgeCursor(branchChar, activeLength - edgeLength)
                    makeSuffixTree(progress, nextCursor)(prefixNode, targetNode)
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
