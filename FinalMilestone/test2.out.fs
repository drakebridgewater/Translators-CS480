variable n 
 fvariable a 
 fvariable b 
 fvariable area 
 fvariable width 
 fvariable x 
 100 n ! n @ 
 0 a ! a @ 
 1 b ! b @ 
 0 area ! area @ 
 a x ! x @ 
 b a x + - n / width ! width @ 
 : whilestmts73  x b < while area x 2 ^ width * + area ! area @ 
 x width + x ! x @ 
 REPEAT ; whilestmts73 . 
 cr cr bye 