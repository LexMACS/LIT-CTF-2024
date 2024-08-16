char*S="flag.txt";
FILE*F;
char B[99];
typedef void V;
typedef V X();
V z(){puts(B);}
V y(){fgets(B,99,F);}
V x(){F=fopen(S,"r");}
[[gnu::destructor]]X x;
[[gnu::destructor]]X y;
[[gnu::destructor]]X z;
