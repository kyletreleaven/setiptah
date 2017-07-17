package setiptah.suffixtree.algorithms

import setiptah.suffixtree.SuffixTrees
import setiptah.suffixtree.SuffixTrees.{Internal, Leaf, Node}

/**
  * Created by ktreleav on 7/4/2017.
  */
trait SuffixTreeAlgorithm {
  def suffixTree(string: String): SuffixTrees.Node
}


trait SuffixTreeBuilder[TNode] {
  def newRoot: TNode
  def addTerminalEdge(node: TNode, startIndex: Int)
  def addInternalEdge(node: TNode, startIndex: Int, length: Int): TNode
}


trait SuffixTreeDriver[TNode] {
  def suffixTree(string: String, builder: SuffixTreeBuilder[TNode]): TNode
}


class SuffixTreeAlgorithmDriverAdapter[TNode](algorithm: SuffixTreeAlgorithm)
  extends SuffixTreeDriver[TNode] {

  def suffixTree(string: String, builder: SuffixTreeBuilder[TNode]): TNode = {
    val implRoot = algorithm.suffixTree(string)

    def process(implNode: Node, targetNode: TNode): Unit = {
      for ( (c, edge) <- implNode.outEdges ) {
        edge.extent match {
          case Leaf => {
            builder.addTerminalEdge(targetNode, edge.startIndex)
          }
          case Internal(length, nextImplNode) => {
            val nextTargetNode = builder.addInternalEdge(targetNode, edge.startIndex, length)
            process(nextImplNode, nextTargetNode)
          }
        }
      }
    }

    val root = builder.newRoot
    process(implRoot, root)

    root
  }
}