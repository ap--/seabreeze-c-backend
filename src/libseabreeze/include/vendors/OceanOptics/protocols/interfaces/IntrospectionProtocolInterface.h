/***************************************************//**
 * @file    IntrospectionProtocolInterface.h
 * @date    January 2017
 * @author  Ocean Optics, Inc.
 *
 * This is a generic interface into introspectionfunctionality
 * at the protocol level, agnostic to any particular protocol.
 * Each Protocol offering this functionality should implement
 * this interface.
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

#ifndef INTROSPECTION_PROTOCOL_INTERFACE_H
#define INTROSPECTION_PROTOCOL_INTERFACE_H

#include "common/buses/Bus.h"
#include "common/exceptions/ProtocolException.h"
#include "common/protocols/ProtocolHelper.h"

namespace seabreeze {

    class IntrospectionProtocolInterface : public ProtocolHelper {
    public:
        IntrospectionProtocolInterface(Protocol *protocol);
        virtual ~IntrospectionProtocolInterface();

		virtual unsigned short getNumberOfPixels(const Bus &bus) = 0;
		virtual std::vector<unsigned int> *getActivePixelRanges(const Bus &bus) = 0;
		virtual std::vector<unsigned int> *getElectricDarkPixelRanges(const Bus &bus) = 0;
		virtual std::vector<unsigned int> *getOpticalDarkPixelRanges(const Bus &bus) = 0;

    };

} /* end namespace seabreeze */

#endif /* INTROSPECTION_PROTOCOL_INTERFACE_H */
