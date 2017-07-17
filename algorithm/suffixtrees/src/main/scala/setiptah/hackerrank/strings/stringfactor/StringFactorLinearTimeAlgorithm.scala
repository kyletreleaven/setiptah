package setiptah.hackerrank.strings.stringfactor

import setiptah.suffixtree.algorithms.{NaiveReference, NaiveSuffixTreeDriver, NodeDisplayExtension, SuffixTreeBuilder}

import scala.collection.mutable

/**
  * Created by ktreleav on 7/17/2017.
  */
object StringFactorLinearTimeAlgorithm extends StringFactorAlgorithm {

  class ScoreNode(
                   val parent: Option[ScoreNode],
                   val startIdx: Int,
                   val length: Int) {
    val outEdges = new mutable.HashSet[ScoreNode]

    var numberOfSuffixes: Int = -1 // just myself, unless reset!
    var score: Int = -1

    def collect(): Seq[ScoreNode] = {
      Seq(this) ++ outEdges.map( _.collect() ).flatten.toSeq
    }

    def debugTree(string: String) = {
      val nodes = collect()
      nodes.map( _.debugMe(string) ).mkString("\n")
    }

    val fmt = "(:start %d, :string %s :ndesc %d)"

    def debugMe(string: String) = {
      fmt.format(startIdx, string.drop(startIdx).take(length), numberOfSuffixes)
    }

    override def toString: String = {
      //val fmt = "(:start %d, :length %d :children [%s]"
      //fmt.format(startIdx, length, outEdges.mkString(", "))
      ""
    }
  }

  def printScoreTree(scoreTree: ScoreNode, string: String): Unit = {
    val indexToNode = scoreTree.collect().toArray
    val nodeToIndex = new mutable.HashMap[ScoreNode,Int]()
    for ( i <- 0 until indexToNode.length ) {
      val node = indexToNode(i)
      nodeToIndex.put( indexToNode(i), i )

      val fmt = "%d: %s starting from %d; ndesc %d"
      val substr = string.drop(node.startIdx).take(node.length)
      println(fmt.format(i, substr, node.startIdx, node.numberOfSuffixes))
    }

    def process(node: ScoreNode): Unit = {
      for ( node_ <- node.outEdges ) {
        println("%d -> %d".format(nodeToIndex(node), nodeToIndex(node_)))
      }
      for ( node_ <- node.outEdges ) {
        process(node_)
      }
    }

    process(scoreTree)
  }

  class ScoreTreeBuilder(string: String) extends SuffixTreeBuilder[ScoreNode] {

    def newRoot: ScoreNode = new ScoreNode(None, 0, 0)

    def addTerminalEdge(node: ScoreNode, startIndex: Int): Unit = {
      val suffixLength = string.length - startIndex

      val targetNode = node.parent match {
        // No parent means whole suffix is being added to the root; start from start index.
        case None => {
          new ScoreNode(Some(node), startIndex, suffixLength)
        }

        // Extends the current prefix.
        case Some(parent) => {
          new ScoreNode(Some(node), node.startIdx, node.length + suffixLength)
        }
      }

      node.outEdges.add(targetNode)
    }

    def addInternalEdge(node: ScoreNode, startIndex: Int, length: Int): ScoreNode = {
      val targetNode = node.parent match {
        case None => {
          new ScoreNode(Some(node), startIndex, length)
        }

        case Some(parent) => {
          new ScoreNode(Some(node), node.startIdx, node.length + length)
        }
      }

      node.outEdges.add(targetNode)
      targetNode
    }
  }

  def score(string: String): (Int, String) = {
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
    //val tree = Ukkonen.suffixTree(string + '$')
    val termString = string + '$'
    val builder = new ScoreTreeBuilder(string)

    // TODO(ktreleav): When Ukkonen algorithm is ready, use it instead!
    // Without Ukkonen or other linear time algorithm, this is not linear time!

    // val scoreTree = new UkkonenDriver[ScoreNode].suffixTree(termString, builder)
    val scoreTree = NaiveSuffixTreeDriver.suffixTree(termString, builder)

    //println(scoreTree)
    //println(scoreTree.debugTree(string))

    // Count up suffixes and score each node
    def process(node: ScoreNode): Unit = {
      node.numberOfSuffixes = if (node.outEdges.size == 0) {
        // leaf node
        1
      }
      else {
        node.outEdges.foreach( process )

        val edges = node.outEdges
        val res = edges.foldLeft(0)( (sum, edge) => sum + edge.numberOfSuffixes )
        //val weights = for ( edge <- edges ) yield { edge.numberOfSuffixes }
        // _.number edges.map( _.numberOfSuffixes ).toList
        //val res = weights.sum

        //val res = node.outEdges.map( _.numberOfSuffixes ).sum
        res
      }

      node.score = node.length * node.numberOfSuffixes
    }

    process(scoreTree)

    if (false) {
      // Just for printing
      val naiveTree = NaiveReference.suffixTree(termString)
      val graphString = new NodeDisplayExtension(naiveTree).readable(termString)

      println(graphString)
      printScoreTree(scoreTree, string)
    }

    // Find highest score
    def bestNode(node: ScoreNode): ScoreNode = {
      if (node.outEdges.size == 0) {
        node
      }
      else {
        val bestDescendant = node.outEdges.map( bestNode(_) ).maxBy( _.score )
        if (bestDescendant.score > node.score)
          bestDescendant
        else
          node
      }
    }

    val winner = bestNode(scoreTree)
    (winner.score, string.drop(winner.startIdx).take(winner.length))
  }

  case class StringTreeNode(string: String, outEdges: List[StringTreeNode])

  def extensionOf(prefix: String)(extension: String) = extension.substring(prefix.length)

  def makeStringTree(scoreTree: ScoreNode, string: String): StringTreeNode = {
    val nodeString = string.substring(scoreTree.startIdx, scoreTree.startIdx + scoreTree.length)
    val outEdges = (scoreTree.outEdges
        .map( makeStringTree(_, string) ).toList
        .sortBy( edge => extensionOf(nodeString)(edge.string) ))

    StringTreeNode(nodeString, outEdges)
  }

  def main(args: Array[String]): Unit = {
    // val string = "aaaa"
    val string = "aaabaaaaba"
    //val string = "abaababaa"

    println(string)

    //val (score, substring) = bestScore(string)
    //println(score, substring)

    // println(bestScoreReference(string))
    println(score(string))

  }
}
