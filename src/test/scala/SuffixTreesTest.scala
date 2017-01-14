/**
  * Created by horus on 1/14/2017.
  */
class SuffixTreesTest extends org.scalatest.FunSuite {
  import SuffixTrees._

  test("Suffix tree empty string is single-node") {
    val tree = suffixTree("")
    assert( tree.outEdges.isEmpty )
  }

  test("Suffix tree one char doesn't crash") {
    val tree = suffixTree("0")
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

  test("Suffix tree has root out-degree equal to number of distinct characters") {
    for ( string <- List("ABAC", "ABCDEFG", "AAAA" ) ) {
      val tree = suffixTree(string)
      val distinct = Set[Char]() ++ string
      assert(tree.outEdges.size == distinct.size)
    }
  }

  test("Suffix tree 'ABAC' doesn't crash") {
    val tree = suffixTree("ABAC")

    assert(tree.outEdges.size == 3)
    assert(true)
  }

  test("")
}
