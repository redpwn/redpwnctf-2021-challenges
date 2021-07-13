#include <stdio.h>
#include <wchar.h>

wchar_t* flag = L"flag{n0t_al1_str1ngs_ar3_sk1nny}";

int main() {
  wchar_t buffer[80];

  wprintf(L"Welcome to flag checker 1.0.\nGive me a flag> ");
  fgetws(buffer, sizeof(buffer) / sizeof(wchar_t),stdin);

  if(wcscmp(flag, buffer) == 0) {
    fputws (L"Correct!",stdout);
  }
  return 0; 
}
