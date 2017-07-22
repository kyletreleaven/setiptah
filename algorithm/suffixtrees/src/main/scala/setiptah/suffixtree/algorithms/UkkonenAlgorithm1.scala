package setiptah.suffixtree.algorithms

import setiptah.suffixtree
import setiptah.suffixtree.DisplayNodeUtil
import setiptah.suffixtree.algorithms.SuffixTrie._
import setiptah.suffixtree.util.{DisplayNodeBuilder, DisplayNodeUtil}

import scala.collection.mutable

/**
  * Created by ktreleav on 7/18/2017.
  */

object UkkonenAlgorithm1Driver extends SuffixTreeDriver {
  import SuffixTrie.{OrdinaryNode, TransitionFunc}

  def suffixTree[TNode](string: String, builder: SuffixTreeBuilder[TNode]): TNode = {
    val trie = UkkonenAlgorithm1.suffixTrie(string)

    val root = builder.newRoot

    def process(node: IdentityNode, node_ : TNode): Unit = {
      for (edge <- trie.g.edges(node)) {
        val TransitionFunc.Edge(_, targetNode, alpha) = edge

        alpha match {
          case Terminal => builder.addTerminalEdge(node_, targetNode.startIdx)

          case Alphabetic(_) => {
            val targetNode_ = builder.addInternalEdge(node_, targetNode.startIdx, 1)
            process(targetNode, targetNode_)
          }
        }
      }
    }

    val OrdinaryNode(identityRoot) = trie.root

    process(identityRoot, root)
    root
  }
}


object UkkonenAlgorithm1 {
  import SuffixTrie._

  def suffixTrie(string: String): SuffixTrie = {
    val temp = string.map(Alphabetic(_)).toList ++ List(Terminal)
    suffixTrie(temp)
  }

  def suffixTrie(string: List[AlphabetExt]): SuffixTrie = {
    val trie = new SuffixTrie

    var top: OrdinaryNode = trie.root

    for ( i <- 0 until string.size ) {
      top = Phase(trie, string).execute(i, top)
    }

    // TODO(ktreleav): Collapse all degree 1 nodes.

    trie
  }

  case class Phase(trie: SuffixTrie, string: List[AlphabetExt]) {
    def execute(i: Int, top: OrdinaryNode): OrdinaryNode = {
      var ti = string(i)
      var oldr_ : OrdinaryNode = OrdinaryNode(null) // doesn't matter... just some init

      var r: Node = top
      while ( !trie.g.isDefined(r, ti) ) {
        // do stuff
        var r_ : OrdinaryNode = {
          val id = new IdentityNode
          id.startIdx = i // maybe?
          OrdinaryNode(id)
        }
        trie.g.update(r, ti, r_)

        if (r != top) {
          trie.f.update(oldr_, r_)
        }

        oldr_ = r_
        r = trie.f(r)
      }

      trie.f.update(oldr_, trie.g(r, ti) )
      trie.g(top, ti) // return new top
    }
  }

  def main(args: Array[String]): Unit = {
    //val trie = UkkonenAlgorithm1.suffixTrie("Hello")

    val string = "BANANA"
    val displayTree = UkkonenAlgorithm1Driver.suffixTree(string, DisplayNodeBuilder(string + "$"))

    val dotGraph = DisplayNodeUtil.dotGraph(displayTree)
    println(dotGraph)
  }
}


// Need to use type classes for Alphabet, Node type, etc.
object SuffixTrie {
  sealed trait Node
  case object Special extends Node
  case class OrdinaryNode(node: IdentityNode) extends Node

  class IdentityNode {
    var startIdx: Int = -1
  }

  sealed trait AlphabetExt
  case class Alphabetic(c: Char) extends AlphabetExt
  case object Terminal extends AlphabetExt

  class TransitionFunc(root: IdentityNode) {
    import TransitionFunc.{Edge}

    val g = new mutable.HashMap[IdentityNode, mutable.HashMap[AlphabetExt,IdentityNode]]

    private def newMap() = new mutable.HashMap[AlphabetExt, IdentityNode]

    def update(node: Node, alpha: AlphabetExt, targetNode: OrdinaryNode): Unit = node match {
      case Special => throw new Error("cannot update special entries")

      case OrdinaryNode(node_) => {
        val OrdinaryNode(targetNode_) = targetNode
        val edges = g.getOrElseUpdate(node_, newMap())
        edges.update(alpha, targetNode_)
      }
    }

    def isDefined(node: Node, alpha: AlphabetExt): Boolean = node match {
      case Special => true
      case OrdinaryNode(node_) => g.contains(node_) && g(node_).contains(alpha)
    }

    def apply(node: Node, alpha: AlphabetExt): OrdinaryNode = node match {
      // whole alphabet from Special goes to root...
      case Special => OrdinaryNode(root)
      case OrdinaryNode(node_) => OrdinaryNode( g(node_)(alpha) )
    }

    def edges(tail: IdentityNode): Seq[Edge] = {
      g(tail).map { case (alpha, head) => Edge(tail, head, alpha) }.toSeq
    }
  }
  object TransitionFunc {
    case class Edge(tail: IdentityNode, head: IdentityNode, label: AlphabetExt)
  }

  //def emptyTrie(): SuffixTrie = new SuffixTrie(new IdentityNode)
}


class SuffixTrie private (rootIdentity: IdentityNode)
  // extends SuffixTreeDriver
{
  import SuffixTrie._

  var root = OrdinaryNode(rootIdentity)
  val g = new TransitionFunc(rootIdentity)
  val f = new mutable.HashMap[Node, Node]
  f.update(root, Special)

  def this() {
    this(new IdentityNode)
  }

  def children(node: IdentityNode): Seq[IdentityNode] = {
    g.edges(node).map ( edge => edge.head )
  }

  def descendants(node: IdentityNode): Seq[IdentityNode] = {
    val temp = children(node)
    temp ++ temp.flatMap( descendants(_) )
  }

  def Q(): Seq[IdentityNode] = {
    Seq(rootIdentity) ++ descendants(rootIdentity)
  }

  // TODO(ktreleav): Turn this into its own driver...
  //  override def toString: String = {
}