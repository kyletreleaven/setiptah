package setiptah.suffixtree.util

import setiptah.suffixtree.algorithms.SuffixTreeBuilder

/**
  * Created by ktreleav on 7/23/2017.
  */
case class DisplayNodeBuilder(string: String) extends SuffixTreeBuilder[DisplayNode] {
  def newRoot: DisplayNode = new DisplayNode

  def addTerminalEdge(node: DisplayNode, startIndex: Int): Unit = {
    node.edges.update(string.substring(startIndex), new DisplayNode)
  }

  def addInternalEdge(node: DisplayNode, startIndex: Int, length: Int): DisplayNode = {
    val targetNode = new DisplayNode
    node.edges.update(string.substring(startIndex, startIndex + length), targetNode)

    targetNode
  }
}
