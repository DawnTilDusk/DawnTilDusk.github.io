#include <iostream>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <cstring>

using namespace std;
long long a[30];

int main(){
	int n;
	a[1] = 1, a[2] = 2;
	for(int i=3; i<=25; i++)
		a[i] = a[i-2] + a[i-1];
	scanf("%d", &n);
	printf("%lld", a[n]);
	return 0;
}
