#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>
#include <algorithm>
using namespace std;

bool f[100001];

int main(){
	int len, n;
	scanf("%d%d", &len, &n);
	for(int i=0; i<=len; i++)
		f[i] = 0;
	for(int i=1; i<=n; i++){
		int l, r;
		scanf("%d%d", &l, &r);
		for(int j=l; j<=r; j++)
			if(!f[j]) f[j] = 1;
	}
//	for(int i=1; i<=len; i++) cout<<f[i]<<endl;
	int cnt = 0;
	for(int i=0; i<=len; i++)
		if(!f[i]) cnt++;
	printf("%d\n", cnt);
	return 0;
}
