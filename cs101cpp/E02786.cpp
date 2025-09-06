#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>
#include <algorithm>

#define mod 32767
using namespace std;

int p[1000001];

int main(){
	p[1] = 1, p[2] = 2;
	for(int i=2; i<=1000000; i++)
		p[i+1] = (2*p[i] + p[i-1])%mod;
	int n;
	scanf("%d", &n);
	for(int i=1; i<=n; i++){
		int t;
		scanf("%d", &t);
		printf("%d\n", p[t]);
	}
	return 0;
}
