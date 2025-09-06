#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>

using namespace std;

int main(){
	int n, cnt = 0;
	int d = 8;
	scanf("%d", &n);
	if(n < 8){
		cout<< n;
		return 0;
	}
	while(d*8 <= n) d*=8;
	while(n){
		printf("%d", n/d);
		n %= d;
		d /= 8;
	}
	for(;d >= 1; d/=8)
		printf("0");
	return 0;
}
