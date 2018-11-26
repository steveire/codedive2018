
void foo()
{
   int a[3] = {0,1,2};
   
   int a2[2 + 1] = {0,1,2};

   constexpr int someSize = 2;
   constexpr int otherSize = 1;

   int a3[someSize + otherSize] = {0,1,2};

   int a4[] = {0,1,2};
}
