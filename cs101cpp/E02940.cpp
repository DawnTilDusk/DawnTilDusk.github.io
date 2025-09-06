#include <iostream>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <cstring>

using namespace std;

int main(){
	int a, n;
	scanf("%d %d", &a, &n);
	long long ans = 0;
	int base = 1;
	for(int i=1; i<=n; i++){
		ans += (n-i+1) * a * base;
		base *= 10;
	}
	printf("%lld\n", ans);
	return 0;
}
