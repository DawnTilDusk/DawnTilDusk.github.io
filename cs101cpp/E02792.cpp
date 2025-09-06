#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>
#include <algorithm>
using namespace std;

int A[10001], B[10001];

int query(int s, int l, int r){
	cout << s << " "<< l << " " << r<< endl;
	if(B[l] > s)
		return 0;
	else if(l == r)
		return s == B[l] ? 1 : 0;
	int mid = (l+r) >> 1;
	return query(s, l, mid) + query(s, mid+1, r);
}

int main(){
	int n;
	cin >> n;
	for(int l=1; l<=n; l++){
		int a, b, s;
		cin >> s >> a;
		for(int i=1; i<=a; i++) cin >> A[i];
		cin >> b;
		for(int i=1; i<=b; i++) cin >> B[i];
		sort(A+1, A+a+1);
		sort(B+1, B+b+1);
		int cnt = 0;
		for(int i=1; i<=a&&A[i]<=s; i++){
			int tmp = query(s - A[i], 1, b);
			if(tmp)
				cnt += tmp;
		}
		printf("%d\n", cnt);
	}
	return 0;
}
