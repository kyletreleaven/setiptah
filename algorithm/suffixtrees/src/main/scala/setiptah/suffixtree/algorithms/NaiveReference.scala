package setiptah.suffixtree.algorithms
import setiptah.hackerrank.strings.StringUtil
import setiptah.suffixtree.SuffixTrees._

import scala.collection.mutable
/**
  * Created by ktreleav on 7/4/2017.
  */

object NaiveSuffixTreeDriver extends SuffixTreeAlgorithmDriverAdapter(NaiveReference)


object OptionUtil {
  def optionEqualsMax[T](equals: (T,T) => Boolean)(i: Option[T], j: Option[T]): Boolean = {
    (i, j) match {
      case (None, None) => true
      case (Some(i_), Some(j_)) => equals(i_, j_)
      case _ => false
    }
  }
}

object SuffixTreeComparison {
  class Node {
    val outEdges = new mutable.HashMap[Char,Edge]
  }

  case class Edge(string: String, target: Option[Node])

  class Builder(string: String) extends SuffixTreeBuilder[Node] {
    def newRoot: Node = new Node

    def addTerminalEdge(node: Node, startIndex: Int): Unit = {
      node.outEdges.update(string(startIndex), Edge(string.substring(startIndex), None))
    }

    def addInternalEdge(node: Node, startIndex: Int, length: Int): Node = {
      val target = new Node
      node.outEdges.update(string(startIndex), Edge(string.substring(startIndex, startIndex + length), Some(target)))
      target
    }
  }

  def equals(edgeA: Edge, edgeB: Edge): Boolean = {
    ((edgeA.string == edgeB.string)
      && OptionUtil.optionEqualsMax[Node](equals)(edgeA.target, edgeB.target))
  }

  def equals(treeA: Node, treeB: Node): Boolean = {
    val keysA = treeA.outEdges.keySet
    val keysB = treeB.outEdges.keySet

    def eq(c: Char): Boolean = {
      val edgeA = treeA.outEdges(c)
      val edgeB = treeB.outEdges(c)
      equals(edgeA, edgeB)
    }

    (keysA.subsetOf(keysB) && keysB.subsetOf(keysA)
      && keysA.forall(eq))
  }
}


object NaiveReference extends App
  with SuffixTreeAlgorithm {
  /** Reference (naive algorithm).
    *
    * @param string
    * @return
    */

  override def suffixTree(string: String) = {
    val edges = (0 until string.length).map(new Edge(_))
    suffixTree(edges.toList, string)
  }

  /**
    * Naive, recursive algorithm.
    * First, group suffixes (edges) by starting character.
    * Then, for all non-trivial groups, create a sub- suffix tree of all edges in the group advanced by one character,
    * and attach that tree to the one being built by a single, one-character edge.
    * (There is a small re-stitching included
    * to combine the one-character stub with the singleton edge of any subtree where applicable.
    *
    * @param edges
    * @param string
    * @return
    */
  def suffixTree(edges: List[Edge], string: String): Node = {
    val root = new Node

    // Create the groupings of edges by first character.
    val grouping = edges.groupBy(e => string(e.startIndex))

    for ((c, group) <- grouping) {
      if (group.size == 1) {
        root.outEdges.put(c, group.head)
      }

      else {
        val example = group.head

        // *all* input edges are of Leaf type *and* have more material in the tail!
        val group_ = group.map(e => new Edge(e.startIndex + 1))
        val subTree = suffixTree(group_, string)

        // Connect the sub suffix tree to this one.
        val nextEdge = if ( subTree.outEdges.size == 1 ) {
          val subTreeEdge = subTree.outEdges.values.head

          subTreeEdge.extent match {
            case Internal(length, target) => new Edge(example.startIndex, Internal(length+1, target))
            case Leaf => {
              throw new Error("sub suffix trees should extend on internal edges only")
            }  // Should not be possible!
          }
        }

        else {
          val charEdge = new Edge(example.startIndex)
          charEdge.extent = Internal(1, subTree)

          charEdge
        }

        root.outEdges.put(c, nextEdge)
      }
    }

    root
  }

  override def main(args: Array[String]): Unit = {
    for ( s <- StringUtil.suffixes("hello") ) {
      println(s)
    }
  }
}
