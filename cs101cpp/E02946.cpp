#include <iostream>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <cstring>

using namespace std;
int s, n;

int main(){
	scanf("%d%d", &s, &n);
	for(int i=1; i<=n; i++){
		string op; int a;
		cin >> op >> a;
		if(op == "multiply") s *= a;
		if(op == "minus") s -= a;
		if(op == "plus") s += a;
	}
	printf("%d\n", s);
	return 0;
}
