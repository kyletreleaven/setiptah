
/**
  * Created by ktreleav on 3/5/17.
  */


sealed trait binop
case object Plus extends binop
case object Times extends binop

sealed trait expr
case class Const(n: Int) extends expr
case class Binop(b: binop, e1: expr, e2: expr) extends expr

sealed trait instr
case class IConst(n: Int) extends instr
case class IBinop(b: binop) extends instr


object StackMachine {
  type prog = List[instr]
  type stack = List[Int]

  def binopDenote(b: binop): (Int,Int) => Int = b match {
    case Plus => (a,b) => a + b
    case Times => (a,b) => a * b
  }

  def expDenote(e: expr): Int = e match {
    case Const(n) => n
    case Binop(b, e1, e2) => binopDenote(b)(expDenote(e1), expDenote(e2))
  }

  def instrDenote(i: instr, s: stack): Option[stack] = i match {
    case IConst(n) => Some(n :: s)
    case IBinop(b) => s match {
      case arg1 :: arg2 :: s_ => Some(binopDenote(b)(arg1, arg2) :: s_)
      case _ => None
    }
  }

  def progDenote(p: prog, s: stack): Option[stack] = p match {
    case Nil => Some(s)
    case i :: p_ => instrDenote(i, s) match {
      case None => None
      case Some(s_) => progDenote(p_, s_)
    }
  }

  def compile(e: expr): prog = e match {
    case Const(n) => IConst(n) :: Nil
    case Binop(b, e1, e2) => compile(e2) ++ compile(e1) ++ List(IBinop(b))
  }

  def main(args: Array[String]): Unit = {
    println("Hello there")

    println(expDenote(Binop(Plus, Const(1), Const(2))))

    val program = List(IConst(3),IConst(4),IBinop(Times))
    println(progDenote(program, List.empty[Int]))

    val e2 = Binop(Times, Binop(Plus, Const(3), Const(2)), Const(4))
    val p2 = compile(e2)

    println(e2)
    println(p2)
    println(progDenote(p2,List.empty[Int]))
  }
}
