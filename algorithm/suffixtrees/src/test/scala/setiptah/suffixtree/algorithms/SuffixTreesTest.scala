package setiptah.suffixtree.algorithms

import setiptah.suffixtree.util.DisplayNodeUtil

/**
  * Created by horus on 1/14/2017.
  */

class SuffixTreesTest extends org.scalatest.FunSuite {
  // def suffixTree(string: String) = NaiveReference.suffixTree(string)
  def suffixTree(string: String) = Ukkonen.suffixTree(string)


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

    val display = new NodeDisplayExtension(tree)

    println(display.readable(string))

    val tree_graph = display.graphmap(string)
    println( DisplayNodeUtil.flatten(tree_graph) )

    DisplayNodeUtil.writeDotGraph(tree_graph)
  }

  ///*
  test("Particular string of a's and b's does not crash.") {
    //suffixTree("aaabaaaaba$")
    suffixTree("AACAAA$")
    // TODO(ktreleav): Show the graph.
  }
  // */

  // how would we test: Every internal node is associated with a suffix link? Is that supposed to be true?

  // can I define a parameterized "class" of tests such as below, and run special cases?
  test("Suffix tree has root out-degree equal to number of distinct characters") {
    val string = "LASIJWEIAGAJRPGAFDSF$"
    val tree = suffixTree(string)
    val distinct = Set[Char]() ++ string
    assert(tree.outEdges.size == distinct.size)

    println( new NodeDisplayExtension(tree).readable(string) )
  }

  def randomChoice[T](array: Array[T]): T = {
    array((array.size * scala.math.random()).toInt)
  }

  val alphabet = "ABCDEFG".toCharArray

  def randomString(n: Int): String = {
    (0 until n).map( _ => randomChoice(alphabet) ).mkString("")
  }

  test("Fuzz test against reference implementation.") {

    def seq = (0 until 10000).map( _ => randomString(6) )

    for ( str_ <- seq ) {
      val str = str_ + '$'
      println(str)

      val compareBuilder = new SuffixTreeComparison.Builder(str)

      val treeRef = NaiveSuffixTreeDriver.suffixTree(str,compareBuilder)
      val treeUkkonen = UkkonenDriver.suffixTree(str, compareBuilder)

      assert(SuffixTreeComparison.equals(treeRef, treeUkkonen))
    }
  }
}
