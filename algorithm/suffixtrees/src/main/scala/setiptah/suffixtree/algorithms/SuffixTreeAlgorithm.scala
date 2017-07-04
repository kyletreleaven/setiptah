package setiptah.suffixtree.algorithms

import setiptah.suffixtree.SuffixTrees

/**
  * Created by ktreleav on 7/4/2017.
  */
trait SuffixTreeAlgorithm {
  def suffixTree(string: String): SuffixTrees.Node
}
