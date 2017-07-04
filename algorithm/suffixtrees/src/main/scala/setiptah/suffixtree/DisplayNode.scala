package setiptah.suffixtree

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
