https://en.wikipedia.org/wiki/Regular_expression#Formal_definition

# Basic

"Or" is bar, i.e., |
Parens () create groupings and demonstrate operator precedence 
? - zero or one occurences
* - zero or more occurences
+ - 1 or more occurences

{n} - exactly n
{min,} - min times or more
{min,max} - between min and max times

# Formally

alphabeta \Sigma

Base regular expressions are sets:

(empty set) - \emptyset
(empty string) - \{ \epsilon \}
(literal character) - \{ a \}

Operations; given R and S

(concatenation) - RS
(alternation), or set union - R|S
(Kleene star) - smallest set such R* that:
	R \subset R*
	\epsilon \in R*
	closed under concat, i.e., R* = R*R*

# Operators to encode


# Pre-processing!
