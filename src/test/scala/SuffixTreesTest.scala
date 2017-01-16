/**
  * Created by horus on 1/14/2017.
  */
class SuffixTreesTest extends org.scalatest.FunSuite {
  import SuffixTrees._

  test("Suffix tree on empty string is simple node") {
    val tree = suffixTree("")
    assert( tree.outEdges.isEmpty )
  }

  test("Suffix tree one char doesn't crash") {
    val tree = suffixTree("A")
  }

  test("Suffix tree 'A' has one leaf edge rooted at 'A'") {
    val tree = suffixTree("A")
    assert(tree.outEdges.size == 1)
    assert(tree.outEdges.contains('A'))
  }

  test("Suffix tree 'AB' has two leaf edges rooted at 'A' and 'B'") {
    val tree = suffixTree("AB")
    assert(tree.outEdges.size == 2)
    assert(tree.outEdges.contains('A'))
    assert(tree.outEdges.contains('B'))
  }

  test("Suffix tree 'ABAC' has three top-level branches") {
    val tree = suffixTree("ABAC")

    assert(tree.outEdges.size == 3)
  }

  test("A bunch of As (and one Z) doesn't crash and has two (2) top-level edges") {
    val tree = suffixTree("AAAAAAAAAAAAAAAAAAAAAAAAAAAZ")

    assert(tree.outEdges.size == 2)
  }

  test("Long string that ends in unique character doesn't crash") {
    val string = "AAABCDEFGHIABGHSJASKLJFAIEOJASDKJEAFGADADSJFL"

    for (n <- 0 to string.length) {
      val substr = string.substring(0, n) + "$"

      val tree = suffixTree(substr)

      println("%s fine...".format(substr))
    }
  }

  test("Long string that ends in unique character doesn't crash; but did until final character...") {
    //val string = "AAABCDEFGHIAB$"
    //val string = "AAABCAB$"

    //val string = "ABCAB$" // PASSES!
    val string = "TRELEAVEN$"

    val tree = suffixTree(string)

    println(tree.readable(string))

    val tree_graph = tree.graphmap(string)
    println( flatten(tree_graph) )

    writeDotGraph(tree_graph)
  }

  def flatten(node: Node2): List[Node2] = {
    List(node) ++ node.edges.values   .flatMap( flatten )
  }

  def listEdges(node: Node2): Unit = {
    val nodes = flatten(node)
    val nodeMap = nodes.zipWithIndex   .toMap

    for ( i: Node2 <- nodes; (e: String,j: Node2) <- i.edges ) {
      println("%d -(%s)->%d".format(nodeMap(i), e, nodeMap(j)))
    }
  }

  def writeDotGraph(node: Node2): Unit = {
    val nodes = flatten(node)
    val nodeMap = nodes.zipWithIndex   .toMap

    println("digraph MYGRAPH{")
    for ( i: Node2 <- nodes; (e: String,j: Node2) <- i.edges ) {
      //println("%d -(%s)->%d".format(nodeMap(i), e, nodeMap(j)))
      println("\t%d -> %d [label=\"%s\"]".format(nodeMap(i), nodeMap(j), e))
    }
    println("}")
  }


  // how would we test: Every internal node is associated with a suffix link? Is that supposed to be true?

  // can I define a parameterized "class" of tests such as below, and run special cases?
  test("Suffix tree has root out-degree equal to number of distinct characters") {
    val string = "LASIJWEIAGAJRPGAFDSF$"
    val tree = suffixTree(string)
    val distinct = Set[Char]() ++ string
    assert(tree.outEdges.size == distinct.size)

    println( tree.readable(string) )
  }
}
