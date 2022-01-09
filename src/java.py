import io
import pathlib
import pkgutil
import contextlib
import datetime
import textwrap
import re
import urllib.request
import urllib.parse

# resources and constants
config_script_path = pathlib.Path(__file__)
config_directory = lambda: config_script_path.parent.parent
resource_directory = lambda: config_directory()/'res'
current_year = lambda: datetime.date.today().year
apache_license_text = lambda: (resource_directory()/'license.txt').read_text('utf-8')
gitignore_text = lambda: (resource_directory()/'java'/'gitignore.txt').read_text('utf-8')

# checkout
project_script_path = None
project_directory = lambda: pathlib.Path(project_script_path).parent.parent
workflows_directory = lambda: project_directory()/'.github'/'workflows'

# repository
repository_name = lambda: project_directory().name
github_repository_url = lambda: f'https://github.com/robertvazan/{repository_name()}' if is_opensource() else None
bitbucket_repository_url = lambda: f'https://bitbucket.org/robertvazan/{repository_name()}'
repository_url = lambda: github_repository_url() if is_opensource() else bitbucket_repository_url()
repository_file_url = lambda path: f'{repository_url()}/blob/master/{path}'
scm_connection = lambda: f'scm:git:{repository_url()}.git'

# general info
pretty_name = lambda: repository_name()
is_opensource = lambda: True

# license
license_id = lambda: 'Apache-2.0' if is_opensource() else None
license_name = lambda: 'Apache License 2.0' if is_opensource() else None
license_url = lambda: repository_file_url('LICENSE') if is_opensource() else None
license_text = lambda: apache_license_text() if is_opensource() else None
inception_year = lambda: current_year()

# maven coordinates
pom_subgroup = lambda: repository_name()
pom_group = lambda: 'com.machinezoo.' + pom_subgroup()
pom_artifact = lambda: repository_name()
pom_version = lambda: (project_directory()/'scripts'/'version.txt').read_text('utf-8').strip()

# website
has_website = lambda: is_opensource()
subdomain = lambda: pom_subgroup()
website = lambda: f'https://{subdomain()}.machinezoo.com/'
homepage = lambda: website()
javadoc_site = lambda: website() + 'javadoc/'
def javadoc_home():
    if not is_module():
        return javadoc_site()
    if is_multi_package():
        return javadoc_site() + module_name() + '/module-summary.html'
    return javadoc_site() + module_name() + '/' + main_package().replace('.', '/') + '/package-summary.html'

# project info
pom_name = lambda: pretty_name()
pom_description = lambda: None

# code structure
module_info_path = lambda: project_directory()/'src'/'main'/'java'/'module-info.java'
is_module = lambda: module_info_path().exists()
module_info_text = lambda: module_info_path().read_text('utf-8')
module_info_matches = lambda pattern: [x.group(1) for x in re.finditer(pattern, module_info_text(), re.MULTILINE)]
module_name = lambda: module_info_matches(r'\bmodule\s+([a-zA-Z0-9_.]+)')[0]
main_package = lambda: module_name() if is_module() else 'com.machinezoo.' + pom_artifact().replace('-', '.')
main_class_name = lambda: None
main_class = lambda: main_package() + '.' + main_class_name() if main_class_name() else None
is_library = lambda: main_class() is None
exported_packages = lambda: module_info_matches(r'^\s+exports\s+([a-zA-Z0-9_.]+);')
is_multi_package = lambda: is_module() and len(exported_packages()) > 1

# build features
jdk_version = lambda: 11
jdk_preview = lambda: False
jdk_parameter_names = lambda: False
maven_central = lambda: is_library() and is_opensource()
test_coverage = lambda: maven_central()
has_javadoc = lambda: maven_central()
jmh_benchmarks = lambda: False
stagean_annotations = lambda: False

# dependencies
dependencies = lambda: None
javadoc_links = lambda: standard_javadoc_links()

# readme
badges = lambda: standard_badges()
project_status = lambda: stable_status() if is_opensource() else unpublished_status()
documentation_links = lambda: standard_documentation_links()
md_description = lambda: homepage_lead() + f'\n\nMore on [homepage]({homepage()}).' if has_website() else pom_description()

def use_xml(xml):
    print_pom(2, xml)

def use(dependency, scope=None, *, classifier=None, exclusions=[]):
    group, artifact, version = dependency.split(':')
    print_pom(2, f'''\
        <dependency>
            <groupId>{group}</groupId>
            <artifactId>{artifact}</artifactId>
            <version>{version}</version>
    ''')
    if scope:
        print_pom(3, f'<scope>{scope}</scope>')
    if classifier:
        print_pom(3, f'<classifier>{classifier}</classifier>')
    if exclusions:
        print_pom(3, '<exclusions>')
        for exclusion in exclusions:
            ex_group, ex_artifact = exclusion.split(':')
            print_pom(4, f'''\
                <exclusion>
                    <groupId>{ex_group}</groupId>
                    <artifactId>{ex_artifact}</artifactId>
                </exclusion>
            ''')
        print_pom(3, '</exclusions>')
    print_pom(2, '</dependency>')

def use_stagean(): use('com.machinezoo.stagean:stagean:1.2.0')
def use_hookless(): use('com.machinezoo.hookless:hookless:0.14.4')
def use_pushmode(): use('com.machinezoo.pushmode:pushmode:0.8.2')
def use_pmdata(): use('com.machinezoo.pmdata:pmdata:0.12.3')

def use_slf4j(): use('org.slf4j:slf4j-api:1.7.32')
def use_fastutil(): use('it.unimi.dsi:fastutil:8.5.6')
def use_commons_collections(): use('org.apache.commons:commons-collections4:4.4')
def use_commons_math(): use('org.apache.commons:commons-math3:3.6.1')
def use_commons_io(): use('commons-io:commons-io:2.11.0')
def use_guava(): use('com.google.guava:guava:31.0.1-jre')
def use_gson(): use('com.google.code.gson:gson:2.8.9')
jackson_version = lambda: '2.13.1'
def use_jackson_cbor():
    use(f'com.fasterxml.jackson.core:jackson-databind:{jackson_version()}')
    use(f'com.fasterxml.jackson.dataformat:jackson-dataformat-cbor:{jackson_version()}')
jmh_version = lambda: '1.34'
def use_jmh():
    use(f'org.openjdk.jmh:jmh-core:{jmh_version()}')
    use(f'org.openjdk.jmh:jmh-generator-annprocess:{jmh_version()}')

def use_junit(): use('org.junit.jupiter:junit-jupiter:5.8.2', 'test')
def use_hamcrest(): use('org.hamcrest:hamcrest:2.2', 'test')
def use_mockito(): use('org.mockito:mockito-core:4.2.0', 'test')
def use_slf4j_test(): use('com.github.valfirst:slf4j-test:2.3.0', 'test')

def standard_javadoc_links():
    if stagean_annotations():
        yield 'https://stagean.machinezoo.com/javadoc/'

def standard_badges():
    if maven_central():
        print(f'[![Maven Central](https://img.shields.io/maven-central/v/{pom_group()}/{pom_artifact()})](https://search.maven.org/artifact/{pom_group()}/{pom_artifact()})')
    if is_opensource():
        print(f'[![Build status]({github_repository_url()}/workflows/build/badge.svg)]({github_repository_url()}/actions/workflows/build.yml)')
    if test_coverage():
        print(f'[![Test coverage](https://codecov.io/gh/robertvazan/{repository_name()}/branch/master/graph/badge.svg)](https://codecov.io/gh/robertvazan/{repository_name()})')

stagean_notice = lambda: ' [Stagean](https://stagean.machinezoo.com/) is used to track progress on class and method level.' if stagean_annotations() else ''
stable_status = lambda: 'Stable and maintained.' + stagean_notice()
experimental_status = lambda: 'Experimental.' + stagean_notice()
obsolete_status = lambda: 'Obsolete. No longer maintained.'
unpublished_status = lambda: 'Experimental. Unpublished.'

def standard_documentation_links():
    if has_website():
        yield 'Homepage', homepage()
    if has_javadoc():
        yield 'Javadoc', javadoc_home()

homepage_html = None
def homepage_lead():
    url = homepage()
    global homepage_html
    if not homepage_html:
        homepage_html = urllib.request.urlopen(url).read().decode('utf-8')
    lead = re.search(r'<p>(.*?)</p>', homepage_html, re.DOTALL).group(1)
    lead = re.sub(r'<code>(.*?)</code>', r'`\1`', lead)
    lead = re.sub(r'''<a\s+href=["']([^'"]*)["']>(.*?)</a>''', lambda m: f'[{m.group(2)}]({urllib.parse.urljoin(url, m.group(1))})', lead, 0, re.DOTALL)
    lead = re.sub(r'<.*?>', '', lead, 0, re.DOTALL)
    return lead

def print_to(path, generator):
    print(f'Generating {path}...')
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as file:
        with contextlib.redirect_stdout(file):
            generator()

def print_lines(text, *, indent='', tabify=False):
    text = textwrap.dedent(text)
    if text[-1:] != '\n':
        text += '\n'
    if tabify:
        for i in range(0, 5):
            text = re.sub('^(\t*) {4}', r'\1\t', text, flags=re.MULTILINE)
    text = textwrap.indent(text, indent)
    print(text, end='')

def capture_output(function):
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        function()
    return f.getvalue()

def print_pom(indent, text):
    print_lines(text, indent=indent * '\t', tabify=True)

def notice():
    print(f"Robert Važan's {pretty_name()}")
    if has_website():
        print(homepage())
    print_lines(f'''\
        Copyright {inception_year()}-{current_year()} Robert Važan and contributors
        Distributed under {license_name()}.
    ''')

def build_workflow():
    print_lines(f'''\
        # Generated by scripts/configure.py
        name: build
        on:
          push:
            branches:
              - master
        jobs:
          build:
            uses: robertvazan/project-config/.github/workflows/java-build.yml@master
            with:
              java-version: {jdk_version()}
              test-coverage: {'true' if test_coverage() else 'false'}
    ''')

def release_workflow():
    # GitHub Actions cannot run the whole release procedure.
    # Releases are initiated by running a script on developer machine, which then triggers this workflow via REST API.
    print_lines(f'''\
        # Generated by scripts/configure.py
        name: release
        on: workflow_dispatch
        jobs:
          release:
            uses: robertvazan/project-config/.github/workflows/java-release.yml@master
            with:
              java-version: {jdk_version()}
            secrets:
              server-password: ${{{{ secrets.MAVEN_SERVER_PASSWORD }}}}
              signing-key: ${{{{ secrets.MAVEN_SIGNING_KEY }}}}
              signing-password: ${{{{ secrets.MAVEN_SIGNING_PASSWORD }}}}
    ''')

def pom():
    print_pom(0, f'''\
        <!-- Generated by scripts/configure.py -->
        <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
            <modelVersion>4.0.0</modelVersion>

            <groupId>{pom_group()}</groupId>
            <artifactId>{pom_artifact()}</artifactId>
            <version>{pom_version()}</version>

            <name>{pom_name()}</name>
    ''')
    if pom_description():
        print_pom(1, f'<description>{pom_description()}</description>')
    if has_website():
        print_pom(1, f'<url>{homepage()}</url>')
    print_pom(1, f'<inceptionYear>{inception_year()}</inceptionYear>')
    if is_opensource():
        print()
        print_pom(1, f'''\
            <licenses>
                <license>
                    <name>{license_id()}</name>
                    <url>{license_url()}</url>
                </license>
            </licenses>
        ''')
    print()
    print_pom(1, f'''\
        <organization>
            <name>Robert Važan</name>
            <url>https://robert.machinezoo.com/</url>
        </organization>
        <developers>
            <developer>
                <name>Robert Važan</name>
                <email>robert.vazan@tutanota.com</email>
                <url>https://robert.machinezoo.com/</url>
            </developer>
        </developers>
    ''')
    if is_opensource():
        print()
        print_pom(1, f'''\
            <scm>
                <connection>{scm_connection()}</connection>
                <developerConnection>{scm_connection()}</developerConnection>
                <url>{repository_url()}</url>
            </scm>
        ''')
    print()
    print_pom(1, f'''\
        <properties>
            <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
            <maven.compiler.release>{jdk_version()}</maven.compiler.release>
        </properties>

        <dependencies>
    ''')
    if stagean_annotations():
        use_stagean()
    dependencies()
    if jmh_benchmarks():
        use_jmh()
    print_pom(1, f'''\
        </dependencies>

        <build>
    ''')
    if (project_directory()/'src'/'main'/'filtered').is_dir():
        print_pom(2, '''\
            <resources>
                <resource>
                    <directory>src/main/filtered</directory>
                    <filtering>true</filtering>
                </resource>
            </resources>
        ''')
    # Needed for Java 11+.
    # Contains fix for https://issues.apache.org/jira/browse/MCOMPILER-289
    print_pom(2, f'''\
        <plugins>
            <plugin>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.8.1</version>
    ''')
    if jdk_preview() or jdk_parameter_names() or jmh_benchmarks():
        print_pom(4, '<configuration>')
        if jdk_preview() or jdk_parameter_names():
            print_pom(5, '<compilerArgs>')
            if jdk_preview():
                print_pom(6, '<compilerArg>--enable-preview</compilerArg>')
            if jdk_parameter_names():
                print_pom(6, '<compilerArg>-parameters</compilerArg>')
            print_pom(5, '</compilerArgs>')
        if jmh_benchmarks():
            # Annotation processors are not picked from classpath, because there is nothing on the classpath in Java 9+.
            # We have to list them here. Otherwise we get the dreaded "Unable to get public no-arg constructor" error.
            print_pom(5, f'''\
                <annotationProcessorPaths>
                    <path>
                        <groupId>org.openjdk.jmh</groupId>
                        <artifactId>jmh-generator-annprocess</artifactId>
                        <version>{jmh_version()}</version>
                    </path>
                </annotationProcessorPaths>
            ''')
        print_pom(4, '</configuration>')
    # Needed for Java 17+.
    print_pom(3, f'''\
        </plugin>
        <plugin>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.0.0-M5</version>
    ''')
    if jdk_preview():
        print_pom(4, '''\
            <configuration>
                <argLine>--enable-preview</argLine>
            </configuration>
        ''')
    print_pom(3, '</plugin>')
    if test_coverage():
        # JaCoCo plugin is needed to generate Codecov report.
        # Configuration taken from: https://github.com/codecov/example-java/blob/master/pom.xml#L38-L56
        print_pom(3, '''\
            <plugin>
                <groupId>org.jacoco</groupId>
                <artifactId>jacoco-maven-plugin</artifactId>
                <version>0.8.7</version>
                <executions>
                    <execution>
                        <id>prepare-agent</id>
                        <goals>
                            <goal>prepare-agent</goal>
                        </goals>
                    </execution>
                    <execution>
                        <id>report</id>
                        <phase>test</phase>
                        <goals>
                            <goal>report</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        ''')
    # In order to release to Maven Central, javadoc has to be generated even if it is empty.
    if has_javadoc() or maven_central():
        print_pom(3, '''\
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-javadoc-plugin</artifactId>
                <version>3.2.0</version>
                <configuration>
                    <notimestamp>true</notimestamp>
                    <bottom>
                        <![CDATA[<!-- No copyright message. -->]]>
                    </bottom>
        ''')
        if list(javadoc_links()):
            # Explicit link list, because detectLinks would cause every CI build to fail.
            # CI build is configured to fail on javadoc warnings and we want to keep that.
            print_pom(5, '<links>')
            for link in javadoc_links():
                print_pom(6, f'<link>{link}</link>')
            print_pom(5, '</links>')
        print_pom(3, '''\
                </configuration>
                <executions>
                    <execution>
                        <id>attach-javadocs</id>
                        <goals>
                            <goal>jar</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        ''')
    if maven_central():
        # Maven Central releases require source, javadoc, staging, and gpg plugins.
        # Nexus does two-phase staging deployment, which is not supported by maven-deploy-plugin.
        print_pom(3, '''\
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-source-plugin</artifactId>
                <version>3.0.1</version>
                <executions>
                    <execution>
                        <id>attach-sources</id>
                        <goals>
                            <goal>jar-no-fork</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <groupId>org.sonatype.plugins</groupId>
                <artifactId>nexus-staging-maven-plugin</artifactId>
                <version>1.6.8</version>
                <extensions>true</extensions>
                <configuration>
                    <serverId>ossrh</serverId>
                    <nexusUrl>https://oss.sonatype.org/</nexusUrl>
                    <autoReleaseAfterClose>true</autoReleaseAfterClose>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-gpg-plugin</artifactId>
                <version>1.6</version>
                <configuration>
                    <gpgArguments>
                        <arg>--pinentry-mode</arg>
                        <arg>loopback</arg>
                    </gpgArguments>
                </configuration>
                <executions>
                    <execution>
                        <id>sign-artifacts</id>
                        <phase>verify</phase>
                        <goals>
                            <goal>sign</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        ''')
    if jmh_benchmarks():
        # Required by JMH architecture. Benchmarks must be compiled into an independent executable JAR file.
        # Filter prevents failure when shading signed dependencies: https://stackoverflow.com/a/6743609
        print_pom(3, '''\
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-shade-plugin</artifactId>
                <version>3.2.3</version>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals>
                            <goal>shade</goal>
                        </goals>
                        <configuration>
                            <outputFile>target/${project.artifactId}-jmh.jar</outputFile>
                            <transformers>
                                <transformer implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer" />
                                <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                    <mainClass>org.openjdk.jmh.Main</mainClass>
                                </transformer>
                            </transformers>
                            <filters>
                                <filter>
                                    <artifact>*:*</artifact>
                                    <excludes>
                                        <exclude>META-INF/*.SF</exclude>
                                        <exclude>META-INF/*.DSA</exclude>
                                        <exclude>META-INF/*.RSA</exclude>
                                    </excludes>
                                </filter>
                            </filters>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        ''')
    print_pom(0, '''\
                </plugins>
            </build>
        </project>
    ''')

def contribution_guidelines():
    print_lines(f'''\
        <!--- Generated by scripts/configure.py --->
        # How to contribute to {pretty_name()}

        Thank you for taking interest in {pretty_name()}. There is nothing surprising about contributing to this project.
        You can stop reading now if you have prior experience contributing to other projects.
        If you are unsure, read the instructions below.

        ## Authoritative repository

        Sources are mirrored on several sites. You can submit issues and pull requests on any mirror.

        * [{repository_name()} @ GitHub]({github_repository_url()})
        * [{repository_name()} @ Bitbucket]({bitbucket_repository_url()})

        ## Issues

        Both bug reports and feature requests are welcome. There is no free support,
        but it's perfectly reasonable to open issues asking for more documentation or better usability.

        ## Pull requests

        Pull requests are generally welcome.
        If you would like to make large or controversial changes, open an issue first to discuss your idea.

        Don't worry about formatting and naming too much. Code will be reformatted after merge.
        Just don't run your formatter on whole source files, because it makes diffs hard to understand.

        ## License

        Your submissions will be distributed under [{license_name()}](LICENSE).
    ''')

def readme():
    print('<!--- Generated by scripts/configure.py --->')
    print(f'# {pretty_name()}')
    if capture_output(badges):
        print()
        badges()
    if md_description():
        print()
        print_lines(md_description())
    print()
    print_lines(f'''\
        ## Status

        {project_status()}
    ''')
    if has_website():
        print()
        print_lines(f'''\
            ## Getting started

            See [homepage]({homepage()}).
        ''')
    if list(documentation_links()):
        print()
        print('## Documentation')
        print()
        for title, url in documentation_links():
            print(f'* [{title}]({url})')
    elif is_opensource():
        print()
        print_lines(f'''\
            ## Documentation

            None yet. Review source code.
        ''')
    if is_opensource():
        print()
        print_lines(f'''\
            ## Feedback

            Bug reports and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

            ## License

            Distributed under [{license_name()}](LICENSE).
        ''')

def gitignore():
    print_lines(gitignore_text())

def license():
    print(license_text(), end='')

def remove_obsolete(path):
    if path.exists():
        print(f'Removing obsolete {path}...')
        path.unlink()

def generate(settings):
    globals().update(settings)
    print_to(project_directory()/'.gitignore', gitignore);
    if is_opensource():
        print_to(project_directory()/'LICENSE', license);
        print_to(project_directory()/'NOTICE', notice)
        print_to(workflows_directory()/'build.yml', build_workflow)
    if maven_central():
        print_to(workflows_directory()/'release.yml', release_workflow)
    print_to(project_directory()/'pom.xml', pom)
    if is_opensource():
        print_to(project_directory()/'CONTRIBUTING.md', contribution_guidelines)
    print_to(project_directory()/'README.md', readme)
    remove_obsolete(project_directory()/'.travis.yml')
    remove_obsolete(workflows_directory()/'maven-release.yml')
    print(f'Updated {pretty_name()} configuration.')
