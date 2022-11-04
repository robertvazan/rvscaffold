exec((config_directory()/'src'/'common.py').read_text())

# resources and constants
lang_directory = lambda: resource_directory()/'java'

# repository
common_repository_name = lambda: repository_name().removesuffix('-java')
scm_connection = lambda: f'scm:git:{repository_url()}.git'

# maven coordinates
pom_subgroup = lambda: project_group()
pom_group = lambda: 'com.machinezoo.' + pom_subgroup()
pom_artifact = lambda: common_repository_name()

# website
subdomain = lambda: pom_subgroup()
javadoc_site = lambda: f'{website()}javadocs/{project_extension() if is_extension() else "core"}/' if is_member_project() else website() + 'javadoc/'
def javadoc_home():
    if not is_module():
        return javadoc_site()
    if is_multi_package():
        return javadoc_site() + module_name() + '/module-summary.html'
    return javadoc_site() + module_name() + '/' + main_package_path() + '/package-summary.html'

# project info
pom_name = lambda: pretty_name()
pom_description = lambda: None

# code structure
module_info_path = lambda: project_directory()/'src'/'main'/'java'/'module-info.java'
is_module = lambda: module_info_path().exists()
module_info_text = lambda: module_info_path().read_text('utf-8')
module_info_matches = lambda pattern: [x.group(1) for x in re.finditer(pattern, module_info_text(), re.MULTILINE)]
module_name = lambda: module_info_matches(r'^(?:open\s+)?module\s+([a-zA-Z0-9_.]+)')[0]
main_package = lambda: module_name() if is_module() else 'com.machinezoo.' + pom_artifact().replace('-', '.')
main_package_path = lambda: main_package().replace('.', '/')
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
has_javadoc = lambda: maven_central() and has_website()
complete_javadoc = lambda: has_javadoc()
jmh_benchmarks = lambda: False
stagean_annotations = lambda: False

# dependencies
dependencies = lambda: None
javadoc_links = lambda: standard_javadoc_links()

# readme
md_description_fallback = lambda: pom_description()
stagean_notice = lambda: ' [Stagean](https://stagean.machinezoo.com/) is used to track progress on class and method level.' if stagean_annotations() else ''
stable_status = lambda: 'Stable and maintained.' + stagean_notice()
experimental_status = lambda: 'Experimental.' + stagean_notice()

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

def define_use(dependency):
    return lambda *args, **kwargs: use(dependency, *args, **kwargs)

use_stagean = define_use('com.machinezoo.stagean:stagean:1.3.0')
use_closeablescope = define_use('com.machinezoo.closeablescope:closeablescope:1.0.0')
use_noexception = define_use('com.machinezoo.noexception:noexception:1.9.0')
use_noexception_slf4j = define_use('com.machinezoo.noexception:noexception-slf4j:1.0.1')
use_hookless = define_use('com.machinezoo.hookless:hookless:0.14.4')
use_pushmode = define_use('com.machinezoo.pushmode:pushmode:0.8.2')
use_pmsite = define_use('com.machinezoo.pmsite:pmsite:0.18.4')
use_pmdata = define_use('com.machinezoo.pmdata:pmdata:0.12.4')

use_slf4j = define_use('org.slf4j:slf4j-api:1.7.32')
use_streamex = define_use('one.util:streamex:0.8.1')
use_fastutil = define_use('it.unimi.dsi:fastutil:8.5.6')
use_commons_lang = define_use('org.apache.commons:commons-lang3:3.12.0')
use_commons_collections = define_use('org.apache.commons:commons-collections4:4.4')
use_commons_math = define_use('org.apache.commons:commons-math3:3.6.1')
use_commons_io = define_use('commons-io:commons-io:2.11.0')
use_guava = define_use('com.google.guava:guava:31.0.1-jre')
use_gson = define_use('com.google.code.gson:gson:2.8.9')
jackson_version = lambda: '2.13.3'
use_jackson = define_use(f'com.fasterxml.jackson.core:jackson-databind:{jackson_version()}')
def use_jackson_cbor():
    use_jackson()
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

def standard_documentation_links():
    yield from common_documentation_links()
    if has_javadoc():
        yield 'Javadoc', javadoc_home()

def documentation_comment():
    if is_library() and not complete_javadoc():
        if has_javadoc():
            print(f'Some APIs are undocumented. You might have to peek in the [source code](src/main/java/{main_package_path()}).')
        else:
            print(f'There is no javadoc yet. See [source code](src/main/java/{main_package_path()}) for available APIs.')

def print_pom(indent, text):
    print_lines(text, indent=indent * '\t', tabify=True)

def build_workflow():
    print_lines(f'''\
        # Generated by scripts/configure.py
        name: build
        on:
          push:
            branches: [ master ]
          pull_request:
            branches: [ master ]
          workflow_dispatch:
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
            <version>{project_version()}</version>

            <name>{pom_name()}</name>
    ''')
    if pom_description():
        print_pom(1, f'<description>{pom_description()}</description>')
    print_pom(1, f'''
        <url>{homepage() if has_website() else repository_url()}</url>
        <inceptionYear>{inception_year()}</inceptionYear>
    ''')
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
    ''')
    if main_class():
        print_pom(2, f'<exec.mainClass>{module_name()}/{main_class()}</exec.mainClass>')
    print_pom(1, f'''\
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
                <version>3.3.1</version>
                <configuration>
                    <notimestamp>true</notimestamp>
        ''')
        if not complete_javadoc() and jdk_version() >= 17:
            print_pom(5, '<doclint>all,-missing</doclint>')
        print_pom(5, '''\
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
        ''')
        if jdk_version() >= 17:
            # Bugs OSSRH-66257 and NEXUS-26993.
            print_pom(4, '''\
                <dependencies>
                    <dependency>
                        <groupId>com.thoughtworks.xstream</groupId>
                        <artifactId>xstream</artifactId>
                        <version>1.4.15</version>
                    </dependency>
                </dependencies>
            ''')
        print_pom(3, '''\
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

def generate():
    if is_opensource():
        print_to(workflows_directory()/'build.yml', build_workflow)
    if maven_central():
        print_to(workflows_directory()/'release.yml', release_workflow)
    print_to(project_directory()/'pom.xml', pom)
    remove_obsolete(project_directory()/'.travis.yml')
    remove_obsolete(workflows_directory()/'maven-release.yml')
    generate_common()
