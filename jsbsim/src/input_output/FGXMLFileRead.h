/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 Module:       FGXMLFileRead.h
 Author:       Jon S. Berndt
 Date started: 02/04/07
 Purpose:      Shared base class that wraps the XML file reading logic

 ------------- Copyright (C) 2007  Jon S. Berndt (jon@jsbsim.org) -------------

 This program is free software; you can redistribute it and/or modify it under
 the terms of the GNU Lesser General Public License as published by the Free Software
 Foundation; either version 2 of the License, or (at your option) any later
 version.

 This program is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
 details.

 You should have received a copy of the GNU Lesser General Public License along with
 this program; if not, write to the Free Software Foundation, Inc., 59 Temple
 Place - Suite 330, Boston, MA  02111-1307, USA.

 Further information about the GNU Lesser General Public License can also be found on
 the world wide web at http://www.gnu.org.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
SENTRY
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

#ifndef FGXMLFILEREAD_HEADER_H
#define FGXMLFILEREAD_HEADER_H

/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
INCLUDES
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

#include <iostream>
#include <fstream>

#include "input_output/FGXMLParse.h"
#include "simgear/misc/sg_path.hxx"
#include "simgear/io/iostreams/sgstream.hxx"

/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
FORWARD DECLARATIONS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

namespace JSBSim {

class FGXMLFileRead {
public:
  FGXMLFileRead(void) {}
  ~FGXMLFileRead(void) {}

  Element* LoadXMLDocument(const SGPath& XML_filename, bool verbose=true)
  {
    return LoadXMLDocument(XML_filename, file_parser, verbose);
  }

  Element* LoadXMLDocument(const SGPath& XML_filename, FGXMLParse& fparse, bool verbose=true)
  {
    sg_ifstream infile;
    SGPath filename(XML_filename);

    if (!filename.isNull()) {
      if (filename.extension().empty())
        filename.concat(".xml");

      infile.open(filename);
      if ( !infile.is_open()) {
        if (verbose) std::cerr << "Could not open file: " << filename << std::endl;
        return 0L;
      }
    } else {
      std::cerr << "No filename given." << std::endl;
      return 0L;
    }

    readXML(infile, fparse, filename.utf8Str());
    Element* document = fparse.GetDocument();
    infile.close();

    return document;
  }

  void ResetParser(void) {file_parser.reset();}

private:
  FGXMLParse file_parser;
};
}
#endif
