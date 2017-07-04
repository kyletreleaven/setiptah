package setiptah.suffixtree

import scala.collection.mutable.HashMap

object SuffixTrees {

  // A suffix tree contains up to two kinds of edges.
  sealed trait EdgeExtent
  case object Leaf extends EdgeExtent
  case class Internal(length: Int, targetNode: Node) extends EdgeExtent

  class Node {
    val outEdges = HashMap.empty[Char, Edge]

    // These are grafted on *just* for Ukkonen's algorithm.
    // Don't use this for any semantics.
    // TODO(ktreleav): Refactor this out into the Ukkonen algorithm.
    var suffixEdge: Option[SuffixEdge] = None

    def nextNode(default: Node) = suffixEdge.map(_.targetNode).getOrElse(default)
  }

  class SuffixEdge(val targetNode: Node)

  class Edge(
              var startIndex: Int,
              var extent: EdgeExtent
            ) {

    def this(startIndex: Int) {
      this(startIndex, Leaf)
    }
  }

  // TODO(ktreleav): Write a comparer.
}
