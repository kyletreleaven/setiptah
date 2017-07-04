import setiptah.suffixtree.algorithms.Ukkonen
/**
  * Created by ktreleav on 7/3/2017.
  */
object StringProblems {

  /**
    * The function L(s,S) = |s| * the number of occurrences of s as a contiguous substring of S.
    *
    */

  def bestScore(string: String): (Int, String) = {
    /**
      * Find a string with maximum score (as above) and compute the score.
      * I believe this can be computed in O(|S|) time by computing a suffix tree using Ukkonen's O(N) algorithm,
      * and then by a node scoring algorithm:
      *
      * Each node in the suffix tree represents a contiguous substring (not a full suffix).
      * I believe the number of occurrences of the substring is precisely equal to the total number of leaf nodes of the sub-tree.
      * The length of the substring easy to compute.
      * The total number of graph elements is O(|S|) and a single traversal should be sufficient to score the nodes and keep track of a winner.
      * TODO(ktreleav): Implement.
      */
    //
    val tree = Ukkonen.suffixTree(string + '$')

    (0, "")
  }
}
