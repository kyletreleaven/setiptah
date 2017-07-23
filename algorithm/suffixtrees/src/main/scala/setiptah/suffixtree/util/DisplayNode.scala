package setiptah.suffixtree.util

import setiptah.suffixtree.algorithms.SuffixTreeBuilder

import scala.collection.mutable.HashMap

/**
  * Created by ktreleav on 7/4/2017.
  */
class DisplayNode {
  var edges = HashMap.empty[String, DisplayNode]

  override def toString: String = {
    if (edges.size == 0) {
      "nil"
    }
    else {
      edges   .mapValues( _.toString )   .toString
    }
  }
}





object DisplayNodeUtil {
  def flatten(node: DisplayNode): List[DisplayNode] = {
    List(node) ++ node.edges.values   .flatMap( flatten )
  }

  // TODO(ktreleav): Deprecate.
  def listEdges(node: DisplayNode): Unit = {
    val nodes = flatten(node)
    val nodeMap = nodes.zipWithIndex   .toMap

    for (i: DisplayNode <- nodes; (e: String,j: DisplayNode) <- i.edges ) {
      println("%d -(%s)->%d".format(nodeMap(i), e, nodeMap(j)))
    }
  }

  def dotGraph(node: DisplayNode): String = {
    val nodes = flatten(node)
    val nodeMap = nodes.zipWithIndex   .toMap

    val sb = new StringBuilder
    sb.append("digraph MYGRAPH{\n")
    for (i: DisplayNode <- nodes; (e: String,j: DisplayNode) <- i.edges ) {
      //println("%d -(%s)->%d".format(nodeMap(i), e, nodeMap(j)))
      sb.append("\t%d -> %d [label=\"%s\"]".format(nodeMap(i), nodeMap(j), e))
      sb.append("\n")
    }
    sb.append("}\n")

    sb.toString()
  }

  def writeDotGraph(node: DisplayNode): Unit = {
    println(dotGraph(node))
  }
}