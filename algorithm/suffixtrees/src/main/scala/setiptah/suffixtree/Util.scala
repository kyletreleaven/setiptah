package setiptah.suffixtree

/**
  * Created by horus on 1/10/2017.
  */

object Util {
  implicit class StringHelper(string: String) {
    def lastIndex: Int = string.length() - 1
  }

  case class Range(start: Int, end: Int) {
    def length = end - start + 1
  }

  def suffixes(s: String): Seq[String] = s match {
    case "" => Seq.empty[String]
    case _ => Seq(s) ++ suffixes(s.tail)
  }
}
