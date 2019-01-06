/**
 * @file sum_3_5.c
 * @author sb
 */

#include <stdio.h>

unsigned long get_series_sum(unsigned long fterm)
{
	/*
	 * In order to find the series of all the numbers divisible by
	 * fterm(the first term of the series), we will be using the formula:
	 * S = (n/2) * (a + l)
	 * where
	 * a = fterm
	 * l = last number divisible by fterm within the limit
	 * x = any term from fterm to the upper limit
	 */
	if (!fterm)
		return 0;

	return 0;
}

int main(void)
{
	printf("Working");
	return 0;
}
