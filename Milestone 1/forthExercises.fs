: p01 ." Hello World" ; 
: p02 10 7 + 3 5 * 12 / - . ;
: p03 10.0e0 7.0e0 F+ 3.0e0 5.0e0 F* 12.0e0 F/ F- f. ;
: p04 10.0e0 7.0e0 F+ 3.0e0 5.0e0 F* 12.0e0 F/ F- f. ;
: p05 10 7.0e0 s>f F+ 3.0e0 5.0e0 F* 12 s>f F/ F- f. ;
: p06 7.0e0 10 { y F: x } y s>f x 3.0e0 5 s>f 12 s>f f/ f* f- f+ f. ;
: p07 5 4 < ." 7" IF CR ." 2" THEN ;
: p08 5 4 > ." 7" IF CR ." 2" THEN ;
: p09 ( ) 5 BEGIN DUP . 1 - DUP 0 = UNTIL DROP  ;
: p10 ( n -- r ) s>f CR CR .s CR f.s ;
: p11 ( fact ) dup 0 <= if 
		drop 1 else 
		dup 1 - recurse * 
		endif .s ;
: p12 ( fib ) dup 0 = if 
		drop 1 else 
		dup 1 = if 
			drop 1 else 
			1 - dup 1 - recurse swap recurse + 
			endif 
		endif .s ;


p01 CR CR clearstack
p02 CR CR clearstack
p03 CR CR clearstack
p04 CR CR clearstack
p05 CR CR clearstack
p06 CR CR clearstack
p07 CR CR clearstack
p08 CR CR clearstack
p09 CR CR clearstack
5 p10 CR CR clearstack
5 p11 CR CR clearstack
5 p12 CR CR clearstack
10 p12 CR CR clearstack

BYE
