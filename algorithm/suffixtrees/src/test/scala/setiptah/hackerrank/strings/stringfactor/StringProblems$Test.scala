package setiptah.hackerrank.strings.stringfactor

import org.scalatest.FunSuite

/**
  * Created by ktreleav on 7/16/2017.
  */
class StringProblems$Test extends FunSuite {

  import setiptah.suffixtree.algorithms

  def refAssert(string: String) = {
    val expected = StringFactorReferenceAlgorithm.score(string)
    val result = StringFactorLinearTimeAlgorithm.score(string)

    assert( result._1 == expected._1 )

    result
  }

  test("Fuzz test 'linear time' algorithm.") {

    def randomAorB() = if ( scala.math.random() < .75 ) 'A' else 'B'

    for ( trial <- 0 until 1000 ) {
      val string = (0 until 100).map( _ => randomAorB()).mkString("")

      val res = refAssert(string)
      println(string, res._1, res._2)
    }
  }

  test("testBestScore") {
    refAssert("aaabaaaaba")
  }

}
