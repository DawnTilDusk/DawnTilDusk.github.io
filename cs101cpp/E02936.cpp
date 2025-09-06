#include <iostream>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <cstring>

using namespace std;

int main(){
	int a[20], n;
	cin >> n;
	bool b[20], flag;
	for(int i=1; i<=n; i++){
		cin >> a[i];
		b[a[i]] = 1;
	}
	flag = !(b[1] && b[2])
			&& !(b[3] && b[4])
			&& !(b[5] ^ b[6])
			&& (b[7] || b[8]);
	cout << flag << endl;
	return 0;
}
