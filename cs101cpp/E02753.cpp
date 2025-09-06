#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>
#include <algorithm>
using namespace std;

long long fib[100001];

int main(){
	fib[1] = fib[2] = 1;
	for(int i=2; i<=25; i++)
		fib[i+1] = fib[i] + fib[i-1];
	int n;
	scanf("%d", &n);
	for(int i=1; i<=n; i++){
		int t;
		scanf("%d", &t);
		printf("%lld\n", fib[t]);
	}
	return 0;
}
