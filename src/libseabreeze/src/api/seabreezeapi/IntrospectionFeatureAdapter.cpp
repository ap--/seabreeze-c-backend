/***************************************************//**
 * @file    IntrospectionFeatureAdapter.cpp
 * @date    January 2017
 * @author  Ocean Optics, Inc.
 *
 * This is a wrapper that allows
 * access to SeaBreeze IntrospectionFeatureInterface instances.
 *
 * LICENSE:
 *
 * SeaBreeze Copyright (C) 2017, Ocean Optics Inc
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject
 * to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *******************************************************/

#include "common/globals.h"
#include "api/seabreezeapi/SeaBreezeAPIConstants.h"
#include "api/seabreezeapi/IntrospectionFeatureAdapter.h"
#include <string.h> /* for memcpy pre c++11 */
#include <vector>

using namespace seabreeze;
using namespace seabreeze::api;
using namespace std;

IntrospectionFeatureAdapter::IntrospectionFeatureAdapter(
	IntrospectionFeatureInterface *intf,
    const FeatureFamily &f,
	Protocol *p,
	Bus *b,
    unsigned short instanceIndex) : FeatureAdapterTemplate<IntrospectionFeatureInterface>(intf, f, p, b, instanceIndex) {

	/* Nothing else to do here, the initialization list takes care of it */
}

IntrospectionFeatureAdapter::~IntrospectionFeatureAdapter() {
	/* This is just a wrapper around existing instances -- nothing to delete */
}

#ifdef _WINDOWS
#pragma warning (disable: 4101) // unreferenced local variable
#endif

// this function is here to follow the same class hierarchy as readActivePixelRanges() etc. so
//  that data flow is easier to see. The function needs no free()

unsigned short IntrospectionFeatureAdapter::getNumberOfPixels(int *errorCode) {
	unsigned short int returnValue;

	// no memory allocated, just pass it through
	try {
		returnValue = this->feature->getNumberOfPixels(*this->protocol, *this->bus);
		SET_ERROR_CODE(ERROR_SUCCESS);
	}
	catch (const FeatureException &fe) {
		returnValue = 0;
		SET_ERROR_CODE(ERROR_TRANSFER_ERROR);
	}
	return returnValue;
}

// these safety functions free the memory generated by readActivePixelRanges() etc. so the
//  calling function doesn't have to
int IntrospectionFeatureAdapter::getActivePixelRanges(int *errorCode, unsigned int *buffer, int bufferLength)
{
	int numberOfShortIntsCopied = 0;

	vector<unsigned int> *cal;

	try {
		cal = this->feature->getActivePixelRanges(*this->protocol, *this->bus);
		int numberOfShortInts = (int)cal->size();
		numberOfShortIntsCopied = (numberOfShortInts < bufferLength) ? numberOfShortInts : bufferLength;
		memcpy(buffer, &((*cal)[0]), numberOfShortIntsCopied * sizeof(unsigned int));

		delete cal;
		SET_ERROR_CODE(ERROR_SUCCESS);
	}
	catch (const FeatureException &fe) {
		SET_ERROR_CODE(ERROR_TRANSFER_ERROR);
		return 0;
	}
	return numberOfShortIntsCopied;
}

int IntrospectionFeatureAdapter::getElectricDarkPixelRanges(int *errorCode, unsigned int *buffer, int bufferLength)
{
	int numberOfShortIntsCopied = 0;

	vector<unsigned int> *cal;

	try {
		cal = this->feature->getElectricDarkPixelRanges(*this->protocol, *this->bus);
		int numberOfShortInts = (int)cal->size();
		numberOfShortIntsCopied = (numberOfShortInts < bufferLength) ? numberOfShortInts : bufferLength;
		memcpy(buffer, &((*cal)[0]), numberOfShortIntsCopied * sizeof(unsigned int));

		delete cal;
		SET_ERROR_CODE(ERROR_SUCCESS);
	}
	catch (const FeatureException &fe) {
		SET_ERROR_CODE(ERROR_TRANSFER_ERROR);
		return 0;
	}
	return numberOfShortIntsCopied;
}

int IntrospectionFeatureAdapter::getOpticalDarkPixelRanges(int *errorCode, unsigned int *buffer, int bufferLength)
{
	int numberOfShortIntsCopied = 0;

	vector<unsigned int> *cal;

	try {
		cal = this->feature->getOpticalDarkPixelRanges(*this->protocol, *this->bus);
		int numberOfShortInts = (int)cal->size();
		numberOfShortIntsCopied = (numberOfShortInts < bufferLength) ? numberOfShortInts : bufferLength;
		memcpy(buffer, &((*cal)[0]), numberOfShortIntsCopied * sizeof(unsigned int));

		delete cal;
		SET_ERROR_CODE(ERROR_SUCCESS);
	}
	catch (const FeatureException &fe) {
		SET_ERROR_CODE(ERROR_TRANSFER_ERROR);
		return 0;
	}
	return numberOfShortIntsCopied;
}
