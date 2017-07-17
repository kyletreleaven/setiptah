package setiptah.hackerrank.strings.stringfactor

/**
  * Created by ktreleav on 7/17/2017.
  */
object StringFactorReferenceAlgorithm extends StringFactorAlgorithm {
  import StringFactorUtil._

  def score(string: String): (Int, String) = {
    (substrings(string)
        .map( subs => (StringFactorUtil.score(subs, string), subs))
        .maxBy( _._1 ))
  }
}
