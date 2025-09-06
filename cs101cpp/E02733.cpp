#include <iostream>
#include <cstdio>
#include <cstring>

using namespace std;

int main(){
	int n;
	cin << n;
	if(n%4 == 0 && !(n%100 == 0 && n%400 !=0))
		cout<< "Y";
	else cout << "N";
	return 0;
}
