from pathlib import Path
from pylode.profiles import OntPub
from pylode import __version__
from rdflib import Graph
import pytest
import re
from pylode.utils import de_space_html


# scope="session" so that this is reused
# without regeneration in this testing session
@pytest.fixture(scope="session")
def fix_html():
    od = OntPub(Path(__file__).parent / "prof.ttl")
    return od.make_html()


def test_sdo(fix_html):
    sdo_expected = """{
          "@graph": [
            {
              "@id": "http://www.w3.org/ns/dx/prof",
              "@type": "https://schema.org/DefinedTermSet",
              "https://schema.org/contributor": [
                "Antoine Isaac",
                "Simon Cox",
                "Alejandra Gonzalez-Beltran",
                "Makx Dekkers"
              ],
              "https://schema.org/creator": [
                {
                  "@id": "_:n8685fd29ed2c4ee3b3341a0f43e2c4c9b1"
                },
                {
                  "@id": "_:n8685fd29ed2c4ee3b3341a0f43e2c4c9b3"
                }
              ],
              "https://schema.org/dateCreated": {
                "@type": "http://www.w3.org/2001/XMLSchema#date",
                "@value": "2018-02-16"
              },
              "https://schema.org/dateModified": {
                "@type": "http://www.w3.org/2001/XMLSchema#date",
                "@value": "2019-10-25"
              },
              "https://schema.org/description": {
                "@language": "en",
                "@value": "This vocabulary is for describing relationships between standards/specifications, profiles of them and supporting artifacts such as validating resources.\\n\\nThis model starts with [http://dublincore.org/2012/06/14/dcterms#Standard](dct:Standard) entities which can either be Base Specifications (a standard not profiling any other Standard) or Profiles (Standards which do profile others). Base Specifications or Profiles can have Resource Descriptors associated with them that defines implementing rules for the it. Resource Descriptors must indicate the role they play (to guide, to validate etc.) and the formalism they adhere to (dct:format) to allow for content negotiation. A vocabulary of Resource Roles are provided alongside this vocabulary but that list is extensible."
              },
              "https://schema.org/name": "Profiles Vocabulary"
            },
            {
              "@id": "_:n8685fd29ed2c4ee3b3341a0f43e2c4c9b1",
              "https://schema.org/affiliation": {
                "@id": "_:n8685fd29ed2c4ee3b3341a0f43e2c4c9b2"
              },
              "https://schema.org/email": {
                "@type": "http://www.w3.org/2001/XMLSchema#anyURI",
                "@value": "nicholas.car@surroundaustralia.com"
              },
              "https://schema.org/identifier": {
                "@id": "http://orcid.org/0000-0002-8742-7730"
              },
              "https://schema.org/name": "Nicholas J. Car"
            },
            {
              "@id": "_:n8685fd29ed2c4ee3b3341a0f43e2c4c9b3",
              "https://schema.org/affiliation": [
                {
                  "@id": "_:n8685fd29ed2c4ee3b3341a0f43e2c4c9b4"
                },
                {
                  "@id": "_:n8685fd29ed2c4ee3b3341a0f43e2c4c9b5"
                }
              ],
              "https://schema.org/email": {
                "@id": "mailto:rob@metalinkage.com.au"
              },
              "https://schema.org/identifier": {
                "@id": "http://orcid.org/0000-0002-7878-2693"
              },
              "https://schema.org/name": "Rob Atkinson"
            }
          ]
        }"""
    g_expected = Graph().parse(data=sdo_expected, format="json-ld")
    sdo_actual = re.findall(
        r"<script([^>]*)>([^<]*)<\/script>", de_space_html(fix_html)
    )[0][1]
    g_actual = Graph().parse(data=sdo_actual, format="json-ld")

    assert g_actual.isomorphic(g_expected)


def test_logo(fix_html):
    html = fix_html
    assert (
        f"""<div id="pylode">
      <p>made by
        <a href="https://github.com/rdflib/pyLODE">
          <span id="p">p</span>
          <span id="y">y</span>
          <span>LODE</span>
        </a>
        <a href="https://github.com/rdflib/pyLODE/release/{__version__}" id="version">{__version__}</a>
        <span> with the </span>
        <a href="https://w3id.org/profile/ontpub" id="profile">OntPub</a>
        <span>profile</span>
      </p>
    </div>"""
        in html
    ), "pyLODE logo not generated correctly"


def test_metadata(fix_html):
    expected = """<div class="section" id="metadata">
        <h1>Profiles Vocabulary</h1>
        <h2>Metadata</h2>
        <dl>
          <div>
            <dt>
              <strong>IRI</strong>
            </dt>
            <dd>
              <code>http://www.w3.org/ns/dx/prof</code>
            </dd>
          </div>
          <div>
            <dt>
              <a class="hover_property" href="http://purl.org/dc/terms/title" title="A name given to the resource. Defined in DCMI Metadata Terms">Title</a>
            </dt>
            <dd><p>Profiles Vocabulary</p></dd>
          </div>
          <div>
            <dt>
              <a class="hover_property" href="http://purl.org/dc/terms/creator" title="An entity responsible for making the resource. Defined in DCMI Metadata Terms">Creator</a>
            </dt>
            <dd>
              <ul>
                <li>
                  <span>
                    <span>Nicholas J. Car</span>
                    <a href="http://orcid.org/0000-0002-8742-7730">
                    <svg width="15px" height="15px" viewBox="0 0 72 72" version="1.1"
                        xmlns="http://www.w3.org/2000/svg"
                        xmlns:xlink="http://www.w3.org/1999/xlink">
                        <title>Orcid logo</title>
                        <g id="Symbols" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                            <g id="hero" transform="translate(-924.000000, -72.000000)" fill-rule="nonzero">
                                <g id="Group-4">
                                    <g id="vector_iD_icon" transform="translate(924.000000, 72.000000)">
                                        <path d="M72,36 C72,55.884375 55.884375,72 36,72 C16.115625,72 0,55.884375 0,36 C0,16.115625 16.115625,0 36,0 C55.884375,0 72,16.115625 72,36 Z" id="Path" fill="#A6CE39"></path>
                                        <g id="Group" transform="translate(18.868966, 12.910345)" fill="#FFFFFF">
                                            <polygon id="Path" points="5.03734929 39.1250878 0.695429861 39.1250878 0.695429861 9.14431787 5.03734929 9.14431787 5.03734929 22.6930505 5.03734929 39.1250878"></polygon>
                                            <path d="M11.409257,9.14431787 L23.1380784,9.14431787 C34.303014,9.14431787 39.2088191,17.0664074 39.2088191,24.1486995 C39.2088191,31.846843 33.1470485,39.1530811 23.1944669,39.1530811 L11.409257,39.1530811 L11.409257,9.14431787 Z M15.7511765,35.2620194 L22.6587756,35.2620194 C32.49858,35.2620194 34.7541226,27.8438084 34.7541226,24.1486995 C34.7541226,18.1301509 30.8915059,13.0353795 22.4332213,13.0353795 L15.7511765,13.0353795 L15.7511765,35.2620194 Z" id="Shape"></path>
                                            <path d="M5.71401206,2.90182329 C5.71401206,4.441452 4.44526937,5.72914146 2.86638958,5.72914146 C1.28750978,5.72914146 0.0187670918,4.441452 0.0187670918,2.90182329 C0.0187670918,1.33420133 1.28750978,0.0745051096 2.86638958,0.0745051096 C4.44526937,0.0745051096 5.71401206,1.36219458 5.71401206,2.90182329 Z" id="Path"></path>
                                        </g>
                                    </g>
                                </g>
                            </g>
                        </g>
                    </svg></a>
                    <span>(
                      <a href="mailto:nicholas.car@surroundaustralia.com">nicholas.car@surroundaustralia.com</a> )
                    </span>
                    <span>
                      <em> of
                        <a href="https://surroundaustralia.com">SURROUND Australia Pty Ltd</a>
                      </em>
                    </span>
                  </span>
                </li>
                <li>
                  <span>
                    <span>Rob Atkinson</span>
                    <a href="http://orcid.org/0000-0002-7878-2693">
                    <svg width="15px" height="15px" viewBox="0 0 72 72" version="1.1"
                        xmlns="http://www.w3.org/2000/svg"
                        xmlns:xlink="http://www.w3.org/1999/xlink">
                        <title>Orcid logo</title>
                        <g id="Symbols" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                            <g id="hero" transform="translate(-924.000000, -72.000000)" fill-rule="nonzero">
                                <g id="Group-4">
                                    <g id="vector_iD_icon" transform="translate(924.000000, 72.000000)">
                                        <path d="M72,36 C72,55.884375 55.884375,72 36,72 C16.115625,72 0,55.884375 0,36 C0,16.115625 16.115625,0 36,0 C55.884375,0 72,16.115625 72,36 Z" id="Path" fill="#A6CE39"></path>
                                        <g id="Group" transform="translate(18.868966, 12.910345)" fill="#FFFFFF">
                                            <polygon id="Path" points="5.03734929 39.1250878 0.695429861 39.1250878 0.695429861 9.14431787 5.03734929 9.14431787 5.03734929 22.6930505 5.03734929 39.1250878"></polygon>
                                            <path d="M11.409257,9.14431787 L23.1380784,9.14431787 C34.303014,9.14431787 39.2088191,17.0664074 39.2088191,24.1486995 C39.2088191,31.846843 33.1470485,39.1530811 23.1944669,39.1530811 L11.409257,39.1530811 L11.409257,9.14431787 Z M15.7511765,35.2620194 L22.6587756,35.2620194 C32.49858,35.2620194 34.7541226,27.8438084 34.7541226,24.1486995 C34.7541226,18.1301509 30.8915059,13.0353795 22.4332213,13.0353795 L15.7511765,13.0353795 L15.7511765,35.2620194 Z" id="Shape"></path>
                                            <path d="M5.71401206,2.90182329 C5.71401206,4.441452 4.44526937,5.72914146 2.86638958,5.72914146 C1.28750978,5.72914146 0.0187670918,4.441452 0.0187670918,2.90182329 C0.0187670918,1.33420133 1.28750978,0.0745051096 2.86638958,0.0745051096 C4.44526937,0.0745051096 5.71401206,1.36219458 5.71401206,2.90182329 Z" id="Path"></path>
                                        </g>
                                    </g>
                                </g>
                            </g>
                        </g>
                    </svg></a>
                    <span>(
                      <a href="mailto:rob@metalinkage.com.au">rob@metalinkage.com.au</a> )
                    </span>
                    <span>
                      <em> of Metalinkage</em>
                    </span>
                  </span>
                </li>
              </ul>
            </dd>
          </div>
          <div>
            <dt>
              <a class="hover_property" href="http://purl.org/dc/terms/contributor" title="An entity responsible for making contributions to the resource. Defined in DCMI Metadata Terms">Contributor</a>
            </dt>
            <dd>
              <ul>
                <li><p>Antoine Isaac</p></li>
                <li><p>Simon Cox</p></li>
                <li><p>Alejandra Gonzalez-Beltran</p></li>
                <li><p>Makx Dekkers</p></li>
              </ul>
            </dd>
          </div>
          <div>
            <dt>
              <a class="hover_property" href="http://purl.org/dc/terms/created" title="Date of creation of the resource. Defined in DCMI Metadata Terms">Date Created</a>
            </dt>
            <dd><p>2018-02-16</p></dd>
          </div>
          <div>
            <dt>
              <a class="hover_property" href="http://purl.org/dc/terms/modified" title="Date on which the resource was changed. Defined in DCMI Metadata Terms">Date Modified</a>
            </dt>
            <dd><p>2019-10-25</p></dd>
          </div>
          <div>
            <dt>
              <a class="hover_property" href="http://www.w3.org/2002/07/owl#versionIRI" title="The property that identifies the version IRI of an ontology. Defined in The OWL 2 Schema vocabulary (OWL 2)">Version Iri</a>
            </dt>
            <dd>
              <a href="#1.0">1.0</a>
            </dd>
          </div>
          <div>
            <dt>
              <a class="hover_property" href="http://www.w3.org/2002/07/owl#versionInfo" title="The annotation property that provides version information for an ontology or another OWL construct. Defined in The OWL 2 Schema vocabulary (OWL 2)">Version Info</a>
            </dt>
            <dd><p>1.0</p></dd>
          </div>
          <div>
            <dt>
              <a class="hover_property" href="http://purl.org/dc/terms/description" title="An account of the resource. Defined in DCMI Metadata Terms">Description</a>
            </dt>
            <dd><p>This vocabulary is for describing relationships between standards/specifications, profiles of them and supporting artifacts such as validating resources.</p>
<p>This model starts with <a href="dct:Standard">http://dublincore.org/2012/06/14/dcterms#Standard</a> entities which can either be Base Specifications (a standard not profiling any other Standard) or Profiles (Standards which do profile others). Base Specifications or Profiles can have Resource Descriptors associated with them that defines implementing rules for the it. Resource Descriptors must indicate the role they play (to guide, to validate etc.) and the formalism they adhere to (dct:format) to allow for content negotiation. A vocabulary of Resource Roles are provided alongside this vocabulary but that list is extensible.</p></dd>
          </div>
        </dl>
      </div>"""
    e = de_space_html(expected)
    a = de_space_html(fix_html)
    # open("expected.html", "w").write(e)
    # open("actual.html", "w").write(a)
    assert e in a, "Metadata section not generated correctly"


def test_classes(fix_html):
    expected = """<div class="section" id="classes"><h2>Classes</h2><div class="property entity" id="ResourceDescriptor"><h3>Resource Descriptor <sup class="sup-c" title="OWL/RDFS Class">c</sup></h3><table><tr><th>IRI</th><td><code>http://www.w3.org/ns/dx/prof/ResourceDescriptor</code>"""
    e = de_space_html(expected)
    a = de_space_html(fix_html)
    assert e in a, "Classes section not generated correctly"


def test_properties(fix_html):
    expected = """<div class="section" id="objectproperties">
        <h2>Object Properties</h2>
        <div class="property entity" id="hasArtifact">
          <h3>has artifact
            <sup class="sup-op" title="OWL Object Property">op</sup>
          </h3>
          <table>
            <tr>
              <th>IRI</th>
              <td>
                <code>http://www.w3.org/ns/dx/prof/hasArtifact</code>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://purl.org/dc/terms/description" title="An account of the resource. Defined in DCMI Metadata Terms">Description</a>
              </th>
              <td><p>The URL of a downloadable file with particulars such as its format and role indicated by the Resource Descriptor</p></td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#domain" title="A domain of the subject property. Defined in The RDF Schema vocabulary (RDFS)">Domain</a>
              </th>
              <td>
                <span>
                  <a href="#ResourceDescriptor">Resource Descriptor</a>
                  <sup class="sup-c" title="OWL/RDFS Class">c</sup>
                </span>
              </td>
            </tr>
          </table>
        </div>
        <div class="property entity" id="isInheritedFrom">
          <h3>is inherited from
            <sup class="sup-op" title="OWL Object Property">op</sup>
          </h3>
          <table>
            <tr>
              <th>IRI</th>
              <td>
                <code>http://www.w3.org/ns/dx/prof/isInheritedFrom</code>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://purl.org/dc/terms/description" title="An account of the resource. Defined in DCMI Metadata Terms">Description</a>
              </th>
              <td><p>A base specification, a Resource Descriptor from which is to be considered a Resource Descriptor for this Profile also</p></td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#domain" title="A domain of the subject property. Defined in The RDF Schema vocabulary (RDFS)">Domain</a>
              </th>
              <td>
                <span>
                  <a href="#ResourceDescriptor">Resource Descriptor</a>
                  <sup class="sup-c" title="OWL/RDFS Class">c</sup>
                </span>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#range" title="A range of the subject property. Defined in The RDF Schema vocabulary (RDFS)">Range</a>
              </th>
              <td>
                <span>
                  <a href="#Profile">Profile</a>
                  <sup class="sup-c" title="OWL/RDFS Class">c</sup>
                </span>
              </td>
            </tr>
          </table>
        </div>
        <div class="property entity" id="isProfileOf">
          <h3>is profile of
            <sup class="sup-op" title="OWL Object Property">op</sup>
          </h3>
          <table>
            <tr>
              <th>IRI</th>
              <td>
                <code>http://www.w3.org/ns/dx/prof/isProfileOf</code>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://purl.org/dc/terms/description" title="An account of the resource. Defined in DCMI Metadata Terms">Description</a>
              </th>
              <td><p>A specification for which this Profile defines constraints, extensions, or which it uses in combination with other specifications, or provides guidance or explanation about its usage</p></td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#subPropertyOf" title="The subject is a subproperty of a property. Defined in The RDF Schema vocabulary (RDFS)">Sub Property Of</a>
              </th>
              <td>
                <span>
                  <a href="#isTransitiveProfileOf">is transitive profile of</a>
                  <sup class="sup-op" title="OWL Object Property">op</sup>
                </span>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#domain" title="A domain of the subject property. Defined in The RDF Schema vocabulary (RDFS)">Domain</a>
              </th>
              <td>
                <span>
                  <a href="#Profile">Profile</a>
                  <sup class="sup-c" title="OWL/RDFS Class">c</sup>
                </span>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#range" title="A range of the subject property. Defined in The RDF Schema vocabulary (RDFS)">Range</a>
              </th>
              <td>
                <a href="http://purl.org/dc/terms/Standard">Standard</a>
              </td>
            </tr>
          </table>
        </div>
        <div class="property entity" id="isTransitiveProfileOf">
          <h3>is transitive profile of
            <sup class="sup-op" title="OWL Object Property">op</sup>
          </h3>
          <table>
            <tr>
              <th>IRI</th>
              <td>
                <code>http://www.w3.org/ns/dx/prof/isTransitiveProfileOf</code>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://purl.org/dc/terms/description" title="An account of the resource. Defined in DCMI Metadata Terms">Description</a>
              </th>
              <td><p>The transitive closure of the prof:isProfileOf property. Relates a profile to another specification that it is a profile of, possibly via a chain of intermediate profiles that are in prof:isProfileOf relationships</p></td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="https://w3id.org/profile/ontdoc/superPropertyOf" title="Inverse of RDFS' subPropertyOf. Defined in Ontology Documentation Profile">Super Property Of</a>
              </th>
              <td>
                <span>
                  <a href="#isProfileOf">is profile of</a>
                  <sup class="sup-op" title="OWL Object Property">op</sup>
                </span>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#domain" title="A domain of the subject property. Defined in The RDF Schema vocabulary (RDFS)">Domain</a>
              </th>
              <td>
                <span>
                  <a href="#Profile">Profile</a>
                  <sup class="sup-c" title="OWL/RDFS Class">c</sup>
                </span>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#range" title="A range of the subject property. Defined in The RDF Schema vocabulary (RDFS)">Range</a>
              </th>
              <td>
                <a href="http://purl.org/dc/terms/Standard">Standard</a>
              </td>
            </tr>
          </table>
        </div>
        <div class="property entity" id="hasResource">
          <h3>has resource
            <sup class="sup-op" title="OWL Object Property">op</sup>
          </h3>
          <table>
            <tr>
              <th>IRI</th>
              <td>
                <code>http://www.w3.org/ns/dx/prof/hasResource</code>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://purl.org/dc/terms/description" title="An account of the resource. Defined in DCMI Metadata Terms">Description</a>
              </th>
              <td><p>A resource which describes the nature of an artifact and the role it plays in relation to the Profile</p></td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#range" title="A range of the subject property. Defined in The RDF Schema vocabulary (RDFS)">Range</a>
              </th>
              <td>
                <span>
                  <a href="#ResourceDescriptor">Resource Descriptor</a>
                  <sup class="sup-c" title="OWL/RDFS Class">c</sup>
                </span>
              </td>
            </tr>
          </table>
        </div>
        <div class="property entity" id="hasRole">
          <h3>has role
            <sup class="sup-op" title="OWL Object Property">op</sup>
          </h3>
          <table>
            <tr>
              <th>IRI</th>
              <td>
                <code>http://www.w3.org/ns/dx/prof/hasRole</code>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://purl.org/dc/terms/description" title="An account of the resource. Defined in DCMI Metadata Terms">Description</a>
              </th>
              <td><p>The function of an artifact described by a Resource Descriptor, such as specification, guidance etc.</p></td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#domain" title="A domain of the subject property. Defined in The RDF Schema vocabulary (RDFS)">Domain</a>
              </th>
              <td>
                <span>
                  <a href="#ResourceDescriptor">Resource Descriptor</a>
                  <sup class="sup-c" title="OWL/RDFS Class">c</sup>
                </span>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#range" title="A range of the subject property. Defined in The RDF Schema vocabulary (RDFS)">Range</a>
              </th>
              <td>
                <span>
                  <a href="http://www.w3.org/2004/02/skos/core#Concept">Concept</a>
                  <sup class="sup-c" title="OWL/RDFS Class">c</sup>
                </span>
              </td>
            </tr>
          </table>
        </div>
      </div>
      <div class="section" id="datatypeproperties">
        <h2>Datatype Properties</h2>
        <div class="property entity" id="hasToken">
          <h3>has token
            <sup class="sup-dp" title="OWL Datatype Property">dp</sup>
          </h3>
          <table>
            <tr>
              <th>IRI</th>
              <td>
                <code>http://www.w3.org/ns/dx/prof/hasToken</code>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://purl.org/dc/terms/description" title="An account of the resource. Defined in DCMI Metadata Terms">Description</a>
              </th>
              <td><p>The preferred identifier for the Profile, for use in circumstances where its URI cannot be used</p></td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#domain" title="A domain of the subject property. Defined in The RDF Schema vocabulary (RDFS)">Domain</a>
              </th>
              <td>
                <span>
                  <a href="#Profile">Profile</a>
                  <sup class="sup-c" title="OWL/RDFS Class">c</sup>
                </span>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#range" title="A range of the subject property. Defined in The RDF Schema vocabulary (RDFS)">Range</a>
              </th>
              <td>
                <a href="http://www.w3.org/2001/XMLSchema#token">xsd:token</a>
              </td>
            </tr>
          </table>
        </div>
      </div>
      <div class="section" id="annotationproperties">
        <h2>Annotation Properties</h2>
        <div class="property entity" id="conformsto">
          <h3>conforms to
            <sup class="sup-ap" title="OWL Annotation Property">ap</sup>
          </h3>
          <table>
            <tr>
              <th>IRI</th>
              <td>
                <code>http://purl.org/dc/terms/conformsTo</code>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#isDefinedBy" title="The definition of the subject resource. Defined in The RDF Schema vocabulary (RDFS)">Is Defined By</a>
              </th>
              <td>
                <a href="http://purl.org/dc/terms/">DCMI Metadata Terms</a>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://purl.org/dc/terms/description" title="An account of the resource. Defined in DCMI Metadata Terms">Description</a>
              </th>
              <td><p>An established standard to which the described resource conforms</p></td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#subPropertyOf" title="The subject is a subproperty of a property. Defined in The RDF Schema vocabulary (RDFS)">Sub Property Of</a>
              </th>
              <td>
                <ul>
                  <li>
                    <a href="http://purl.org/dc/elements/1.1/relation">dc:relation</a>
                  </li>
                  <li>
                    <span>
                      <a href="http://purl.org/dc/terms/relation">Relation</a>
                      <sup class="sup-p" title="RDF Property">p</sup>
                    </span>
                  </li>
                </ul>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#range" title="A range of the subject property. Defined in The RDF Schema vocabulary (RDFS)">Range</a>
              </th>
              <td>
                <a href="http://purl.org/dc/terms/Standard">Standard</a>
              </td>
            </tr>
          </table>
        </div>
        <div class="property entity" id="format">
          <h3>format
            <sup class="sup-ap" title="OWL Annotation Property">ap</sup>
          </h3>
          <table>
            <tr>
              <th>IRI</th>
              <td>
                <code>http://purl.org/dc/terms/format</code>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#subPropertyOf" title="The subject is a subproperty of a property. Defined in The RDF Schema vocabulary (RDFS)">Sub Property Of</a>
              </th>
              <td>
                <a href="http://purl.org/dc/elements/1.1/format">dc:format</a>
              </td>
            </tr>
            <tr>
              <th>
                <a class="hover_property" href="http://www.w3.org/2000/01/rdf-schema#range" title="A range of the subject property. Defined in The RDF Schema vocabulary (RDFS)">Range</a>
              </th>
              <td>
                <a href="http://purl.org/dc/terms/MediaTypeOrExtent">Media Type or Extent</a>
              </td>
            </tr>
          </table>
        </div>
      </div>"""
    e = de_space_html(expected)
    a = de_space_html(fix_html)
    open("expected.html", "w").write(e)
    open("actual.html", "w").write(a)
    assert e in a, "Properties section not generated correctly"


def test_namespaces(fix_html):
    expected = """<div id="namespaces">
        <h2>Namespaces</h2>
        <dl>
          <dt id=":">:</dt>
          <dd>
            <code>http://www.w3.org/ns/dx/prof/</code>
          </dd>
          <dt id="dc">dc</dt>
          <dd>
            <code>http://purl.org/dc/elements/1.1/</code>
          </dd>
          <dt id="dct">dct</dt>
          <dd>
            <code>http://purl.org/dc/terms/</code>
          </dd>
          <dt id="ns1">ns1</dt>
          <dd>
            <code>http://www.w3.org/ns/dx/</code>
          </dd>
          <dt id="owl">owl</dt>
          <dd>
            <code>http://www.w3.org/2002/07/owl#</code>
          </dd>
          <dt id="rdf">rdf</dt>
          <dd>
            <code>http://www.w3.org/1999/02/22-rdf-syntax-ns#</code>
          </dd>
          <dt id="rdfs">rdfs</dt>
          <dd>
            <code>http://www.w3.org/2000/01/rdf-schema#</code>
          </dd>
          <dt id="sdo">sdo</dt>
          <dd>
            <code>https://schema.org/</code>
          </dd>
          <dt id="skos">skos</dt>
          <dd>
            <code>http://www.w3.org/2004/02/skos/core#</code>
          </dd>
          <dt id="xsd">xsd</dt>
          <dd>
            <code>http://www.w3.org/2001/XMLSchema#</code>
          </dd>
        </dl>
      </div>"""
    assert expected in fix_html, "Namespaces section not generated correctly"


def test_legend(fix_html):
    assert (
        """      <div id="legend">
        <h2>Legend</h2>
        <table class="entity">
          <tr>
            <td>
              <sup class="sup-c" title="OWL/RDFS Class">c</sup>
            </td>
            <td>Classes</td>
          </tr>
          <tr>
            <td>
              <sup class="sup-op" title="OWL Object Property">op</sup>
            </td>
            <td>Object Properties</td>
          </tr>
          <tr>
            <td>
              <sup class="sup-dp" title="OWL Datatype Property">dp</sup>
            </td>
            <td>Datatype Properties</td>
          </tr>
          <tr>
            <td>
              <sup class="sup-ap" title="OWL Annotation Property">ap</sup>
            </td>
            <td>Annotation Properties</td>
          </tr>
        </table>
      </div>"""
        in fix_html
    ), "Legend section not generated correctly"


def test_toc(fix_html):
    expected = """<div id="toc">
      <h3>Table of Contents</h3>
      <ul class="first">
        <li>
          <h4>
            <a href="#metadata">Metadata</a>
          </h4>
        </li>
        <li>
          <h4>
            <a href="#classes">Classes</a>
          </h4>
          <ul class="second">
            <li>
              <a href="#ResourceDescriptor">Resource Descriptor</a>
            </li>
            <li>
              <a href="#ResourceRole">Resource Role</a>
            </li>
            <li>
              <a href="#Profile">Profile</a>
            </li>
          </ul>
        </li>
        <li>
          <h4>
            <a href="#objectproperties">Object Properties</a>
          </h4>
          <ul class="second">
            <li>
              <a href="#hasArtifact">has artifact</a>
            </li>
            <li>
              <a href="#isInheritedFrom">is inherited from</a>
            </li>
            <li>
              <a href="#isProfileOf">is profile of</a>
            </li>
            <li>
              <a href="#isTransitiveProfileOf">is transitive profile of</a>
            </li>
            <li>
              <a href="#hasResource">has resource</a>
            </li>
            <li>
              <a href="#hasRole">has role</a>
            </li>
          </ul>
        </li>
        <li>
          <h4>
            <a href="#datatypeproperties">Datatype Properties</a>
          </h4>
          <ul class="second">
            <li>
              <a href="#hasToken">has token</a>
            </li>
          </ul>
        </li>
        <li>
          <h4>
            <a href="#annotationproperties">Annotation Properties</a>
          </h4>
          <ul class="second">
            <li>
              <a href="#conformsto">conforms to</a>
            </li>
            <li>
              <a href="#format">format</a>
            </li>
          </ul>
        </li>
        <li>
          <h4>
            <a href="#namespaces">Namespaces</a>
          </h4>
          <ul class="second">
            <li>
              <a href="#"></a>
            </li>
            <li>
              <a href="#dc">dc</a>
            </li>
            <li>
              <a href="#dct">dct</a>
            </li>
            <li>
              <a href="#ns1">ns1</a>
            </li>
            <li>
              <a href="#owl">owl</a>
            </li>
            <li>
              <a href="#rdf">rdf</a>
            </li>
            <li>
              <a href="#rdfs">rdfs</a>
            </li>
            <li>
              <a href="#sdo">sdo</a>
            </li>
            <li>
              <a href="#skos">skos</a>
            </li>
            <li>
              <a href="#xsd">xsd</a>
            </li>
          </ul>
        </li>
        <li>
          <h4>
            <a href="#legend">Legend</a>
          </h4>
          <ul class="second"></ul>
        </li>
      </ul>
    </div>"""
    assert expected in fix_html, "ToC logo not generated correctly"
