import scala.collection.mutable.{HashMap}

/**
  * Created by horus on 1/10/2017.
  */

case class Range(start: Int, end: Int) {
  def length = end - start + 1
}

object SuffixTrees {

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


  def suffixTree(string: List[Char]): Node = {
    val root = new Node

    // called per suffix --- gives back (state, next remainder)
    def suffixAction(
                      nextIndex: Int,
                      state: LatentVariables,
                      latestInsert: Option[Node])
    : (LatentVariables, Int) = {

    }

    def charAction(
                    nextIndex: Int,
                    state: LatentVariables)
    : LatentVariables = {



    }

    val start = LatentVariables(root, None, 0)

    // perform actions
    (0 until string.length).foldLeft(start)((state, k) => charAction(k, state))

    root
  }

  def suffixTree(s: String): Node = {
    val strExt: List[Char] = Nil
      //s.toList .map(Simple) ++ Terminal
    suffixTree(strExt)
  }

  def main(args: Array[String]): Unit = {
    println("Hello")

    println(suffixTree("Hello"))
  }
}
