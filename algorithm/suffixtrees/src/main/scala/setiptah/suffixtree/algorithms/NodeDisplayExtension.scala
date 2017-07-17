package setiptah.suffixtree.algorithms

import setiptah.suffixtree.DisplayNode
import setiptah.suffixtree.SuffixTrees.{Edge, Internal, Leaf, Node}

/**
  * Created by ktreleav on 7/16/2017.
  */
class NodeDisplayExtension(node: Node) {
  def readable(string: String)
  : String = graphmap(string).toString()

  def graphmap(string: String): DisplayNode = {
    val displayNode = new DisplayNode

    displayNode.edges = node.outEdges map {
      case (c: Char, edge: Edge) => {
        val prefixStart = edge.startIndex

        edge.extent match {

          case Leaf => {
            val prefixEnd = string.length
            (string.substring(prefixStart, prefixEnd), new DisplayNode)
          }

          case Internal(length, target) => {
            val prefixEnd = prefixStart + length
            (string.substring(prefixStart, prefixEnd),
              new NodeDisplayExtension(target).graphmap(string))
          }
        }
      }
    }

    displayNode
  }
}
