import pkgutil
import pathlib
import contextlib
import textwrap
import re
import io
import datetime
import urllib.request
import urllib.parse
import uuid

def resource_bytes(path): return pkgutil.get_data('rvscaffold', path)
def resource_text(path): return resource_bytes(path).decode("utf-8")
def current_year(): return datetime.date.today().year

def capture_output(function):
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        function()
    return f.getvalue()

def print_lines(text, *, indent='', tabify=False):
    text = textwrap.dedent(text)
    if text[-1:] != '\n':
        text += '\n'
    if tabify:
        for i in range(0, 5):
            text = re.sub('^(\t*) {4}', r'\1\t', text, flags=re.MULTILINE)
    text = textwrap.indent(text, indent)
    print(text, end='')

class Repository:
    # checkout
    # def script_path_text(self): pass
    def script_path(self): return pathlib.Path(self.script_path_text())
    def path(self): return self.script_path().parent.parent
    def relative_path(self, path): return path.relative_to(self.path())
    def workflows_directory(self): return self.path()/'.github'/'workflows'

    def print_to(self, path, generator):
        path = self.path()/path
        print(f'Generating {self.relative_path(path)}...')
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as file:
            with contextlib.redirect_stdout(file):
                generator()

    def remove_obsolete(self, path):
        path = self.path()/path
        if path.exists():
            print(f'Removing obsolete {self.relative_path(path)}...')
            path.unlink()

    # remote repository
    def github_repository_url(self): return f'https://github.com/robertvazan/{self.repository_name()}' if self.is_opensource() else None
    def bitbucket_repository_url(self): return f'https://bitbucket.org/robertvazan/{self.repository_name()}'
    def repository_url(self): return self.github_repository_url() if self.is_opensource() else self.bitbucket_repository_url()
    def repository_file_url(self, path): return f'{self.repository_url()}/blob/master/{path}'
    def repository_dir_url(self, path): return f'{self.repository_url()}/tree/master/{path}'

    # general info
    def repository_name(self): return self.path().name
    def stripped_repository_name(self): return self.repository_name() # without language suffix
    def pretty_name(self): return self.repository_name()
    def is_opensource(self): return True
    def project_version(self): return (self.path()/'scripts'/'version.txt').read_text('utf-8').strip()

    # extension projects
    def project_group(self): return self.stripped_repository_name().partition('-')[0]
    def project_extension(self): return self.stripped_repository_name().partition('-')[2] if '-' in self.stripped_repository_name() else None
    def is_extension(self): return self.project_extension()
    def is_member_project(self): return self.is_extension()

    # gitignore
    # def gitignore_text(self): pass
    def print_gitignore(self): print_lines(self.gitignore_text())

    # license
    def inception_year(self): return current_year()
    def license_id(self): return 'Apache-2.0' if self.is_opensource() else None
    def license_name(self): return 'Apache License 2.0' if self.is_opensource() else None
    def license_url(self): return self.repository_file_url('LICENSE') if self.is_opensource() else None
    def apache_license_text(self): return resource_text('license.txt')
    def license_text(self): return self.apache_license_text() if self.is_opensource() else None
    def print_license(self): print(self.license_text(), end='')
    def print_copyright(self):
        print(f"Robert Važan's {self.pretty_name()}")
        if self.has_website():
            print(self.homepage())
        print_lines(f'''\
            Copyright {self.inception_year()}-{current_year()} Robert Važan and contributors
            Distributed under {self.license_name()}.
        ''')
    def notice_text(self): None
    def print_notice(self):
        print(f"Robert Važan's {self.pretty_name()}")
        print(f'Copyright {self.inception_year()}-{current_year()} Robert Važan and contributors')
        print()
        print_lines(self.notice_text())

    # website
    def has_website(self): return self.is_opensource()
    def subdomain(self): return self.project_group()
    def website(self): return f'https://{self.subdomain()}.machinezoo.com/'
    def homepage(self): return self.website() + (self.project_extension() if self.is_extension() else '')
    def homepage_lead(self):
        url = self.homepage()
        if not hasattr(self, 'homepage_html'):
            self.homepage_html = urllib.request.urlopen(url).read().decode('utf-8')
            self.homepage_html = re.sub(r'<aside.*?</aside>', '', self.homepage_html, flags=re.DOTALL)
        lead = re.search(r'<p>(.*?)</p>', self.homepage_html, re.DOTALL).group(1)
        lead = re.sub(r'<code>(.*?)</code>', r'`\1`', lead)
        lead = re.sub(r'''<a\s+href=["']([^'"]*)["']>(.*?)</a>''', lambda m: f'[{m.group(2)}]({urllib.parse.urljoin(url, m.group(1))})', lead, 0, re.DOTALL)
        lead = re.sub(r'<.*?>', '', lead, 0, re.DOTALL)
        return lead

    # readme
    def print_badges(self): pass
    def stable_status(self): return 'Stable and maintained.'
    def experimental_status(self): return 'Experimental.'
    def obsolete_status(self): return 'Obsolete. No longer maintained.'
    def unpublished_status(self): return 'Experimental. Unpublished.'
    def project_status(self): return self.experimental_status() if self.is_opensource() else self.unpublished_status()
    def documentation_links(self):
        if self.has_website():
            yield 'Homepage', self.homepage()
    def md_description_fallback(self): return None
    def md_description(self): return self.homepage_lead() + f'\n\nMore on [homepage]({self.homepage()}).' if self.has_website() else self.md_description_fallback()
    def print_documentation_comment(self): pass
    def embeddable_readme(self): return False
    def readme_url(self, path): return self.repository_file_url(path) if self.embeddable_readme() else path
    def readme_dir_url(self, path): return self.repository_dir_url(path) if self.embeddable_readme() else path + '/'
    def print_readme(self):
        print('<!--- Generated by scripts/configure.py --->')
        if self.is_opensource():
            print('[![SWUbanner](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner2-direct.svg)](https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md)')
            print()
        print(f'# {self.pretty_name()}')
        if capture_output(self.print_badges):
            print()
            self.print_badges()
        if self.md_description():
            print()
            print_lines(self.md_description())
        print()
        print('## Status')
        print()
        print_lines(self.project_status())
        if self.has_website():
            print()
            print_lines(f'''\
                ## Getting started

                See [homepage]({self.homepage()}).
            ''')
        if list(self.documentation_links()) or capture_output(self.print_documentation_comment):
            print()
            print('## Documentation')
            if list(self.documentation_links()):
                print()
                for title, url in self.documentation_links():
                    print(f'* [{title}]({url})')
            if capture_output(self.print_documentation_comment):
                print()
                self.print_documentation_comment()
        elif self.is_opensource():
            print()
            print_lines(f'''\
                ## Documentation

                None yet. Review source code.
            ''')
        if self.is_opensource():
            print()
            print_lines(f'''\
                ## Feedback

                Bug reports and pull requests are welcome. See [CONTRIBUTING.md]({self.readme_url('CONTRIBUTING.md')}).

                ## License

                Distributed under [{self.license_name()}]({self.readme_url('LICENSE')}).
            ''')

    def print_contributing(self):
        print_lines(f'''\
            <!--- Generated by scripts/configure.py --->
            # How to contribute to {self.pretty_name()}

            Thank you for taking interest in {self.pretty_name()}. This document provides guidance for contributors.

            ## Authoritative repository

            Sources are mirrored on several sites. You can submit issues and pull requests on any mirror.

            * [{self.repository_name()} @ GitHub]({self.github_repository_url()})
            * [{self.repository_name()} @ Bitbucket]({self.bitbucket_repository_url()})

            ## Issues

            Both bug reports and feature requests are welcome. There is no free support,
            but it's perfectly reasonable to open issues asking for more documentation or better usability.

            ## Pull requests

            Pull requests are generally welcome.
            If you would like to make large or controversial changes, open an issue first to discuss your idea.

            Don't worry about formatting and naming too much. Code will be reformatted after merge.
            Just don't run your formatter on whole source files, because it makes diffs hard to understand.

            ## Generated code

            Some files in this repository are generated by [configure.py](scripts/configure.py),
            which in turn uses author's personal [rvscaffold](https://github.com/robertvazan/rvscaffold) repository.
            The intent is to enforce conventions and to reduce maintenance burden.
            If you need to modify generated files, just do so manually and I will update `configure.py` after merge.

            ## License

            Your submissions will be distributed under [{self.license_name()}](LICENSE).
        ''')

    def generate_files(self):
        self.print_to('.gitignore', self.print_gitignore)
        if self.is_opensource():
            self.print_to('LICENSE', self.print_license)
            self.print_to('COPYRIGHT', self.print_copyright)
            self.print_to('CONTRIBUTING.md', self.print_contributing)
        if self.notice_text():
            self.print_to('NOTICE', self.print_notice)
        else:
            self.remove_obsolete('NOTICE')
        self.print_to('README.md', self.print_readme)

    def generate(self):
        self.generate_files()
        print(f'Updated {self.pretty_name()} configuration.')

def print_to_pom(indent, text):
    print_lines(text, indent=indent * '\t', tabify=True)

class JavaDependencyExclusion:
    def __init__(self, dependency):
        self.group, self.artifact = dependency.split(':')
    def print_pom_fragment(self):
        print_to_pom(4, f'''\
            <exclusion>
                <groupId>{self.group}</groupId>
                <artifactId>{self.artifact}</artifactId>
            </exclusion>
        ''')

class JavaDependency:
    def __init__(self, dependency, scope=None, *, classifier=None, exclusions=[]):
        self.group, self.artifact, self.version = dependency.split(':')
        self.scope = scope
        self.classifier = classifier
        self.exclusions = [JavaDependencyExclusion(x) for x in exclusions]
    def print_pom_fragment(self):
        print_to_pom(2, f'''\
            <dependency>
                <groupId>{self.group}</groupId>
                <artifactId>{self.artifact}</artifactId>
                <version>{self.version}</version>
        ''')
        if self.scope:
            print_to_pom(3, f'<scope>{self.scope}</scope>')
        if self.classifier:
            print_to_pom(3, f'<classifier>{self.classifier}</classifier>')
        if self.exclusions:
            print_to_pom(3, '<exclusions>')
            for exclusion in self.exclusions:
                exclusion.print_pom_fragment()
            print_to_pom(3, '</exclusions>')
        print_to_pom(2, '</dependency>')

class Java(Repository):
    # repository
    def gitignore_text(self): return resource_text('gitignore-java.txt')
    def stripped_repository_name(self): return self.repository_name().removesuffix('-java')

    # project info
    def pom_subgroup(self): return self.project_group()
    def pom_group(self): return 'com.machinezoo.' + self.pom_subgroup()
    def pom_artifact(self): return self.stripped_repository_name()
    def pom_name(self): return self.pretty_name()
    def pom_description(self): return None
    def scm_connection(self): return f'scm:git:{self.repository_url()}.git'

    # build features
    def jdk_version(self): return 11
    def jdk_preview(self): return False
    def jdk_parameter_names(self): return False
    def maven_central(self): return self.is_library() and self.is_opensource()
    def test_coverage(self): return self.maven_central()
    def has_javadoc(self): return self.maven_central() and self.has_website()
    def complete_javadoc(self): return self.has_javadoc()
    def jmh_benchmarks(self): return False
    def stagean_annotations(self): return False

    # code structure
    def module_info_path(self): return self.path()/'src'/'main'/'java'/'module-info.java'
    def is_module(self): return self.module_info_path().exists()
    def module_info_text(self): return self.module_info_path().read_text('utf-8')
    def module_info_matches(self, pattern): return [x.group(1) for x in re.finditer(pattern, self.module_info_text(), re.MULTILINE)]
    def module_name(self): return self.module_info_matches(r'^(?:open\s+)?module\s+([a-zA-Z0-9_.]+)')[0]
    def main_package(self): return self.module_name() if self.is_module() else 'com.machinezoo.' + self.pom_artifact().replace('-', '.')
    def main_package_path(self): return self.main_package().replace('.', '/')
    def main_class_name(self): return None
    def main_class(self): return self.main_package() + '.' + self.main_class_name() if self.main_class_name() else None
    def is_library(self): return self.main_class() is None
    def exported_packages(self): return self.module_info_matches(r'^\s+exports\s+([a-zA-Z0-9_.]+);')
    def is_multi_package(self): return self.is_module() and len(self.exported_packages()) > 1

    # website
    def subdomain(self): return self.pom_subgroup()
    def javadoc_site(self):
        if self.is_member_project():
            return f'{self.website()}javadocs/{self.project_extension() if self.is_extension() else "core"}/'
        else:
            return self.website() + 'javadoc/'
    def javadoc_home(self):
        if not self.is_module():
            return self.javadoc_site()
        if self.is_multi_package():
            return self.javadoc_site() + self.module_name() + '/module-summary.html'
        return self.javadoc_site() + self.module_name() + '/' + self.main_package_path() + '/package-summary.html'

    # readme
    def print_badges(self):
        super().print_badges()
        if self.maven_central():
            g = self.pom_group()
            a = self.pom_artifact()
            print(f'[![Maven Central](https://img.shields.io/maven-central/v/{g}/{a})](https://central.sonatype.com/artifact/{g}/{a})')
        if self.is_opensource():
            u = self.github_repository_url()
            print(f'[![Build status]({u}/workflows/build/badge.svg)]({u}/actions/workflows/build.yml)')
        if self.test_coverage():
            n = self.repository_name()
            print(f'[![Test coverage](https://codecov.io/gh/robertvazan/{n}/branch/master/graph/badge.svg)](https://codecov.io/gh/robertvazan/{n})')
    def md_description_fallback(self): return self.pom_description()
    def documentation_links(self):
        yield from super().documentation_links()
        if self.has_javadoc():
            yield 'Javadoc', self.javadoc_home()
    def print_documentation_comment(self):
        if self.is_library() and not self.complete_javadoc():
            if self.has_javadoc():
                print(f'Some APIs are undocumented. You might have to peek in the [source code](src/main/java/{self.main_package_path()}).')
            else:
                print(f'There is no javadoc yet. See [source code](src/main/java/{self.main_package_path()}) for available APIs.')
    def stagean_notice(self):
        if self.stagean_annotations():
            return ' [Stagean](https://stagean.machinezoo.com/) is used to track progress on class and method level.'
        else:
            return ''
    def stable_status(self): return 'Stable and maintained.' + self.stagean_notice()
    def experimental_status(self): return 'Experimental.' + self.stagean_notice()

    # dependencies
    def dependencies(self):
        if self.stagean_annotations():
            yield self.use_stagean()
        if self.jmh_benchmarks():
            yield from self.use_jmh()
    def javadoc_links(self):
        if self.stagean_annotations():
            yield 'https://stagean.machinezoo.com/javadoc/'
    def use(self, *args, **kwargs): return JavaDependency(*args, **kwargs)
    @staticmethod
    def define_use(dependency):
        if isinstance(dependency, list):
            return lambda self, *args, **kwargs: [d(self, *args, **kwargs) for d in dependency]
        elif isinstance(dependency, str):
            return lambda self, *args, **kwargs: self.use(dependency, *args, **kwargs)
        else:
            return lambda self, *args, **kwargs: self.use(dependency(self), *args, **kwargs)

    # my own libraries
    use_stagean = define_use('com.machinezoo.stagean:stagean:1.3.0')
    use_closeablescope = define_use('com.machinezoo.closeablescope:closeablescope:1.0.1')
    use_noexception = define_use('com.machinezoo.noexception:noexception:1.9.1')
    use_noexception_slf4j = define_use('com.machinezoo.noexception:noexception-slf4j:1.0.2')
    use_hookless = define_use('com.machinezoo.hookless:hookless:0.16.1')
    use_hookless_time = define_use('com.machinezoo.hookless:hookless-time:0.1.0')
    use_hookless_prefs = define_use('com.machinezoo.hookless:hookless-prefs:0.1.0')
    use_hookless_noexception = define_use('com.machinezoo.hookless:hookless-noexception:0.1.0')
    use_hookless_collections = define_use('com.machinezoo.hookless:hookless-collections:0.1.0')
    use_pushmode = define_use('com.machinezoo.pushmode:pushmode:0.8.3')
    use_pmsite = define_use('com.machinezoo.pmsite:pmsite:0.18.6')
    use_ladybugformatters = define_use('com.machinezoo.ladybugformatters:ladybugformatters:0.1.1')
    use_remorabindings = define_use('com.machinezoo.remorabindings:remorabindings:0.2.1')
    use_meerkatwidgets = define_use('com.machinezoo.meerkatwidgets:meerkatwidgets:0.2.0')
    use_foxcache = define_use('com.machinezoo.foxcache:foxcache:0.1.3')
    use_pmdata = define_use('com.machinezoo.pmdata:pmdata:0.13.0')

    # commonly used libraries
    use_slf4j = define_use('org.slf4j:slf4j-api:2.0.9')
    use_streamex = define_use('one.util:streamex:0.8.2')
    use_fastutil = define_use('it.unimi.dsi:fastutil:8.5.12')
    use_commons_lang = define_use('org.apache.commons:commons-lang3:3.13.0')
    use_commons_collections = define_use('org.apache.commons:commons-collections4:4.4')
    use_commons_math = define_use('org.apache.commons:commons-math3:3.6.1')
    use_commons_io = define_use('commons-io:commons-io:2.15.0')
    use_commons_text = define_use('org.apache.commons:commons-text:1.10.0')
    use_guava = define_use('com.google.guava:guava:32.1.3-jre')
    use_gson = define_use('com.google.code.gson:gson:2.10.1')
    def jackson_version(self): return '2.15.3'
    use_jackson = define_use(lambda self: f'com.fasterxml.jackson.core:jackson-databind:{self.jackson_version()}')
    use_jackson_cbor = define_use([
        use_jackson,
        define_use(lambda self: f'com.fasterxml.jackson.dataformat:jackson-dataformat-cbor:{self.jackson_version()}')
    ])
    def jmh_version(self): return '1.37'
    use_jmh = define_use([
        define_use(lambda self: f'org.openjdk.jmh:jmh-core:{self.jmh_version()}'),
        define_use(lambda self: f'org.openjdk.jmh:jmh-generator-annprocess:{self.jmh_version()}')
    ])

    # common test libraries
    def use_junit(self): return self.use('org.junit.jupiter:junit-jupiter:5.10.1', 'test')
    def use_hamcrest(self): return self.use('org.hamcrest:hamcrest:2.2', 'test')
    def use_mockito(self): return self.use('org.mockito:mockito-core:5.7.0', 'test')
    def use_slf4j_test(self): return self.use('com.github.valfirst:slf4j-test:3.0.1', 'test')

    def print_pom(self):
        print_to_pom(0, f'''\
            <!-- Generated by scripts/configure.py -->
            <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
                <modelVersion>4.0.0</modelVersion>

                <groupId>{self.pom_group()}</groupId>
                <artifactId>{self.pom_artifact()}</artifactId>
                <version>{self.project_version()}</version>

                <name>{self.pom_name()}</name>
        ''')
        if self.pom_description():
            print_to_pom(1, f'<description>{self.pom_description()}</description>')
        print_to_pom(1, f'''
            <url>{self.homepage() if self.has_website() else self.repository_url()}</url>
            <inceptionYear>{self.inception_year()}</inceptionYear>
        ''')
        if self.is_opensource():
            print()
            print_to_pom(1, f'''\
                <licenses>
                    <license>
                        <name>{self.license_id()}</name>
                        <url>{self.license_url()}</url>
                    </license>
                </licenses>
            ''')
        print()
        print_to_pom(1, f'''\
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
        if self.is_opensource():
            print()
            print_to_pom(1, f'''\
                <scm>
                    <connection>{self.scm_connection()}</connection>
                    <developerConnection>{self.scm_connection()}</developerConnection>
                    <url>{self.repository_url()}</url>
                </scm>
            ''')
        print()
        print_to_pom(1, f'''\
            <properties>
                <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
                <maven.compiler.release>{self.jdk_version()}</maven.compiler.release>
        ''')
        if self.main_class():
            print_to_pom(2, f'<exec.mainClass>{self.module_name()}/{self.main_class()}</exec.mainClass>')
        print_to_pom(1, f'''\
            </properties>

            <dependencies>
        ''')
        for dependency in self.dependencies():
            dependency.print_pom_fragment()
        print_to_pom(1, f'''\
            </dependencies>

            <build>
        ''')
        if (self.path()/'src'/'main'/'filtered').is_dir():
            print_to_pom(2, '''\
                <resources>
                    <resource>
                        <directory>src/main/filtered</directory>
                        <filtering>true</filtering>
                    </resource>
                </resources>
            ''')
        # Needed for Java 11+.
        # Contains fix for https://issues.apache.org/jira/browse/MCOMPILER-289
        print_to_pom(2, f'''\
            <plugins>
                <plugin>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <version>3.11.0</version>
        ''')
        if self.jdk_preview() or self.jdk_parameter_names() or self.jmh_benchmarks():
            print_to_pom(4, '<configuration>')
            if self.jdk_preview() or self.jdk_parameter_names():
                print_to_pom(5, '<compilerArgs>')
                if self.jdk_preview():
                    print_to_pom(6, '<compilerArg>--enable-preview</compilerArg>')
                if self.jdk_parameter_names():
                    print_to_pom(6, '<compilerArg>-parameters</compilerArg>')
                print_to_pom(5, '</compilerArgs>')
            if self.jmh_benchmarks():
                # Annotation processors are not picked from classpath, because there is nothing on the classpath in Java 9+.
                # We have to list them here. Otherwise we get the dreaded "Unable to get public no-arg constructor" error.
                print_to_pom(5, f'''\
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.openjdk.jmh</groupId>
                            <artifactId>jmh-generator-annprocess</artifactId>
                            <version>{self.jmh_version()}</version>
                        </path>
                    </annotationProcessorPaths>
                ''')
            print_to_pom(4, '</configuration>')
        # Needed for Java 17+.
        print_to_pom(3, f'''\
            </plugin>
            <plugin>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.2</version>
        ''')
        if self.jdk_preview():
            print_to_pom(4, '''\
                <configuration>
                    <argLine>--enable-preview</argLine>
                </configuration>
            ''')
        print_to_pom(3, '</plugin>')
        if self.test_coverage():
            # JaCoCo plugin is needed to generate Codecov report.
            # Configuration taken from: https://github.com/codecov/example-java/blob/master/pom.xml#L38-L56
            print_to_pom(3, '''\
                <plugin>
                    <groupId>org.jacoco</groupId>
                    <artifactId>jacoco-maven-plugin</artifactId>
                    <version>0.8.11</version>
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
        if self.has_javadoc() or self.maven_central():
            print_to_pom(3, '''\
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-javadoc-plugin</artifactId>
                    <version>3.6.2</version>
                    <configuration>
                        <notimestamp>true</notimestamp>
            ''')
            if not self.complete_javadoc() and self.jdk_version() >= 17:
                print_to_pom(5, '<doclint>all,-missing</doclint>')
            print_to_pom(5, '''\
                <bottom>
                    <![CDATA[<!-- No copyright message. -->]]>
                </bottom>
            ''')
            if list(self.javadoc_links()):
                # Explicit link list, because detectLinks would cause every CI build to fail.
                # CI build is configured to fail on javadoc warnings and we want to keep that.
                print_to_pom(5, '<links>')
                for link in self.javadoc_links():
                    print_to_pom(6, f'<link>{link}</link>')
                print_to_pom(5, '</links>')
            print_to_pom(3, '''\
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
        if self.maven_central():
            # Maven Central releases require source, javadoc, staging, and gpg plugins.
            # Nexus does two-phase staging deployment, which is not supported by maven-deploy-plugin.
            print_to_pom(3, '''\
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-source-plugin</artifactId>
                    <version>3.3.0</version>
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
            if self.jdk_version() >= 17:
                # Bugs OSSRH-66257 and NEXUS-26993.
                # Not going to be fixed: https://github.com/sonatype/nexus-public/issues/110
                # New plugin in development: https://central.sonatype.org/publish-ea/publish-ea-guide/#publishing-by-uploading-a-bundle
                print_to_pom(4, '''\
                    <dependencies>
                        <dependency>
                            <groupId>com.thoughtworks.xstream</groupId>
                            <artifactId>xstream</artifactId>
                            <version>1.4.15</version>
                        </dependency>
                    </dependencies>
                ''')
            print_to_pom(3, '''\
                </plugin>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-gpg-plugin</artifactId>
                    <version>3.1.0</version>
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
        if self.jmh_benchmarks():
            # Required by JMH architecture. Benchmarks must be compiled into an independent executable JAR file.
            # Filter prevents failure when shading signed dependencies: https://stackoverflow.com/a/6743609
            print_to_pom(3, '''\
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-shade-plugin</artifactId>
                    <version>3.5.1</version>
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
        print_to_pom(0, '''\
                    </plugins>
                </build>
            </project>
        ''')

    def print_build_workflow(self):
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
                runs-on: ubuntu-latest
                steps:
                  - uses: actions/checkout@v2
                  - uses: actions/setup-java@v2
                    with:
                      distribution: temurin
                      java-version: {self.jdk_version()}
                      cache: maven
                  - name: Maven
                    run: |
                      # GPG must be skipped, because CI server does not have release GPG key.
                      # Failure on javadoc warnings is enabled only in CI builds,
                      # so that warnings specific to one JDK version do not break independent builds.
                      # Printing maven version (-V) helps diagnose CI-specific build behavior.
        ''')
        goals = ['install']
        if self.test_coverage():
            print_lines('# JaCoCo phase is needed to create code coverage report that will be later uploaded to Codecov.', indent='          ')
            goals.append('jacoco:report')
        print_lines(f'mvn {" ".join(goals)} -Dgpg.skip=true -Dmaven.javadoc.failOnWarnings=true -B -V', indent='          ')
        if self.test_coverage():
            print_lines('- uses: codecov/codecov-action@v2', indent='      ')

    def print_release_workflow(self):
        # GitHub Actions cannot run the whole release procedure.
        # Releases are initiated by running a script on developer machine, which then triggers this workflow via REST API.
        print_lines(f'''\
            # Generated by scripts/configure.py
            name: release
            on: workflow_dispatch
            jobs:
              release:
                runs-on: ubuntu-latest
                steps:
                  - uses: actions/checkout@v2
                  - uses: actions/setup-java@v2
                    with:
                      distribution: temurin
                      java-version: {self.jdk_version()}
                      server-id: ossrh
                      server-username: MAVEN_SERVER_USERNAME
                      server-password: MAVEN_SERVER_PASSWORD
                      gpg-private-key: ${{{{ secrets.MAVEN_SIGNING_KEY }}}}
                      gpg-passphrase: MAVEN_SIGNING_PASSWORD
                      cache: maven
                  - name: Maven
                    # Printing maven version (-V) helps diagnose GitHub-specific build behavior.
                    run: mvn -B -V deploy
                    env:
                      MAVEN_SERVER_USERNAME: robertvazan
                      MAVEN_SERVER_PASSWORD: ${{{{ secrets.MAVEN_SERVER_PASSWORD }}}}
                      MAVEN_SIGNING_PASSWORD: ${{{{ secrets.MAVEN_SIGNING_PASSWORD }}}}
        ''')

    def generate_files(self):
        super().generate_files()
        if self.is_opensource():
            self.print_to(self.workflows_directory()/'build.yml', self.print_build_workflow)
        if self.maven_central():
            self.print_to(self.workflows_directory()/'release.yml', self.print_release_workflow)
        self.print_to('pom.xml', self.print_pom)
        self.remove_obsolete('.travis.yml')
        self.remove_obsolete(self.workflows_directory()/'maven-release.yml')

def print_to_csproj(indent, text):
    print_lines(text, indent=indent * '  ')

class NetDependency:
    def __init__(self, dependency):
        self.package, self.version = dependency.split(':')
    def print_csproj_fragment(self):
        print_to_csproj(2, f'<PackageReference Include="{self.package}" Version="{self.version}" />')

class Net(Repository):
    # repository
    def gitignore_text(self): return resource_text('gitignore-net.txt')
    def stripped_repository_name(self): return self.repository_name().removesuffix('-net')

    # project name
    def root_namespace(self): return self.repository_name()
    def assembly_name(self): return self.root_namespace()
    def pretty_name(self): return self.root_namespace()
    def project_path(self): return self.path()/self.root_namespace()
    def test_path(self): return self.path()/f'{self.root_namespace()}.Tests'

    # code structure
    def is_library(self): return not (self.project_path()/'Program.cs').exists()
    def sln_projects(self):
        yield self.root_namespace()
        if self.has_tests():
            yield f'{self.root_namespace()}.Tests'
    def resources(self): return []
    def test_resources(self): return []

    # project info
    def nuget_title(self): return self.pretty_name()
    def nuget_description(self): return None
    def nuget_tags(self): return None
    def nuget_icon(self): return 'icon.png' if (self.project_path()/'icon.png').exists() else None

    # build features
    def target_framework(self): return '5.0' if self.is_library() else '6.0'
    def backport_frameworks(self): return []
    def target_frameworks(self): return [self.target_framework(), *self.backport_frameworks()]
    def target_framework_names(self): return ['netstandard' + v.replace('.', '') if v.startswith('2.') else 'net' + v for v in self.target_frameworks()]
    def test_framework(self): return '6.0'
    def lang_version(self): return '10'
    def nuget_release(self): return self.is_library() and self.is_opensource()
    def has_tests(self): return self.is_library()

    # readme
    def md_description_fallback(self): return self.nuget_description()
    def embeddable_readme(self): return self.is_opensource()
    def print_badges(self):
        super().print_badges()
        if self.nuget_release():
            print(f'[![Nuget](https://img.shields.io/nuget/v/{self.root_namespace()})](https://www.nuget.org/packages/{self.root_namespace()}/)')
        if self.is_opensource():
            print(f'[![Build status]({self.github_repository_url()}/workflows/build/badge.svg)]({self.github_repository_url()}/actions/workflows/build.yml)')
    def documentation_links(self):
        yield from super().documentation_links()
        if self.is_library():
            yield 'XML doc comments', self.readme_dir_url(self.root_namespace())

    # dependencies
    def dependencies(self): return []
    def test_dependencies(self):
        yield self.use_nunit()
        yield self.use_nunit_adapter()
        yield self.use_mstest()
    def use(self, dependency): return NetDependency(dependency)
    def define_use(dependency): return lambda self: self.use(dependency)

    # commonly used libraries
    use_nunit = define_use('NUnit:3.13.3')
    use_nunit_adapter = define_use('NUnit3TestAdapter:4.2.1')
    use_mstest = define_use('Microsoft.NET.Test.Sdk:17.2.0')

    def print_csproj(self):
        print_lines(f'''\
            <!-- Generated by scripts/configure.py -->
            <Project Sdk="Microsoft.NET.Sdk">
              <PropertyGroup>
        ''')
        if self.backport_frameworks():
            print_to_csproj(2, f'<TargetFrameworks>{";".join(self.target_framework_names())}</TargetFrameworks>')
        else:
            print_to_csproj(2, f'<TargetFramework>{self.target_framework_names()[0]}</TargetFramework>')
        print_to_csproj(2, f'''\
                <CheckEolTargetFramework>false</CheckEolTargetFramework>
                <LangVersion>{self.lang_version()}</LangVersion>
                <EnableNETAnalyzers>true</EnableNETAnalyzers>
                <Version>{self.project_version()}</Version>
                <Title>{self.nuget_title()}</Title>
        ''')
        if not self.is_library():
            print_to_csproj(2, '<OutputType>Exe</OutputType>')
        if self.assembly_name() != self.root_namespace():
            print_to_csproj(2, f'<AssemblyName>{self.assembly_name()}</AssemblyName>')
        print_to_csproj(2, f'''\
            <Authors>robertvazan</Authors>
            <RepositoryUrl>{self.repository_url()}</RepositoryUrl>
            <PackageProjectUrl>{self.homepage() if self.has_website() else self.repository_url()}</PackageProjectUrl>
        ''')
        if self.nuget_description():
            print_to_csproj(2, f'<Description>{self.nuget_description()}</Description>')
        if self.nuget_tags():
            print_to_csproj(2, f'<PackageTags>{self.nuget_tags()}</PackageTags>')
        if self.is_opensource():
            print_to_csproj(2, f'<PackageLicenseExpression>{self.license_id()}</PackageLicenseExpression>')
        if self.nuget_release():
            print_to_csproj(2, f'<PackageReadmeFile>README.md</PackageReadmeFile>')
        if self.nuget_icon():
            print_to_csproj(2, f'<PackageIcon>{self.nuget_icon()}</PackageIcon>')
        if not self.nuget_release():
            print_to_csproj(2, '<IsPackable>false</IsPackable>')
        if self.is_library():
            print_to_csproj(2, '<GenerateDocumentationFile>true</GenerateDocumentationFile>')
        print_to_csproj(1, '</PropertyGroup>')
        if self.has_tests():
            print_to_csproj(1, f'''\
                <ItemGroup>
                  <InternalsVisibleTo Include="{self.root_namespace()}.Tests" />
                </ItemGroup>
            ''')
        if self.nuget_release() or self.nuget_icon() or self.resources():
            print_to_csproj(1, '<ItemGroup>')
            if self.nuget_release():
                print_to_csproj(2, '<None Include="../README.md" Pack="true" PackagePath="/" />')
            if self.nuget_icon():
                print_to_csproj(2, f'<None Include="{self.nuget_icon()}" Pack="true" PackagePath="/" />')
            if self.resources():
                for resource in self.resources():
                    print_to_csproj(2, f'<EmbeddedResource Include="{resource}" />')
            print_to_csproj(1, '</ItemGroup>')
        if self.dependencies():
            print_to_csproj(1, '<ItemGroup>')
            for dependency in self.dependencies():
                dependency.print_csproj_fragment()
            print_to_csproj(1, '</ItemGroup>')
        print('</Project>')

    def print_test_csproj(self):
        print_lines(f'''\
            <!-- Generated by scripts/configure.py -->
            <Project Sdk="Microsoft.NET.Sdk">
              <PropertyGroup>
                <TargetFramework>net{self.test_framework()}</TargetFramework>
                <CheckEolTargetFramework>false</CheckEolTargetFramework>
                <LangVersion>{self.lang_version()}</LangVersion>
                <EnableNETAnalyzers>true</EnableNETAnalyzers>
                <IsPackable>false</IsPackable>
                <RootNamespace>{self.root_namespace()}</RootNamespace>
              </PropertyGroup>
              <ItemGroup>
                <ProjectReference Include="../{self.root_namespace()}/{self.root_namespace()}.csproj" />
              </ItemGroup>
              <ItemGroup>
        ''')
        for dependency in self.test_dependencies():
            dependency.print_csproj_fragment()
        print_to_csproj(1, '</ItemGroup>')
        if self.test_resources():
            print_to_csproj(1, '<ItemGroup>')
            for resource in self.test_resources():
                print_to_csproj(2, f'<EmbeddedResource Include="{resource}" />')
            print_to_csproj(1, '</ItemGroup>')
        print('</Project>')

    def guid(self, project):
        author = uuid.uuid5(uuid.NAMESPACE_DNS, 'machinezoo.com')
        repository = uuid.uuid5(author, self.repository_name())
        return uuid.uuid5(repository, project)

    def print_sln(self):
        print_lines('''\
            # Generated by scripts/configure.py
            Microsoft Visual Studio Solution File, Format Version 12.00
        ''')
        for project in self.sln_projects():
            print_lines(f'''\
                Project("{{{self.guid(project)}}}") = "{project}", "{project}/{project}.csproj", "{{{self.guid(project)}}}"
                EndProject
            ''')
        print_lines('''\
            Global
                GlobalSection(SolutionConfigurationPlatforms) = preSolution
                    Debug|Any CPU = Debug|Any CPU
                    Release|Any CPU = Release|Any CPU
                EndGlobalSection
                GlobalSection(ProjectConfigurationPlatforms) = postSolution
        ''', tabify=True)
        for project in self.sln_projects():
            print_lines(f'''\
                {{{self.guid(project)}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
                {{{self.guid(project)}}}.Debug|Any CPU.Build.0 = Debug|Any CPU
                {{{self.guid(project)}}}.Release|Any CPU.ActiveCfg = Release|Any CPU
                {{{self.guid(project)}}}.Release|Any CPU.Build.0 = Release|Any CPU
            ''', indent='\t\t')
        print_lines('''\
                EndGlobalSection
            EndGlobal
        ''', tabify=True)

    def print_build_workflow(self):
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
                uses: robertvazan/rvscaffold/.github/workflows/net-build.yml@master
                with:
                  dotnet-version: {self.test_framework()}
        ''')

    def print_release_workflow(self):
        # GitHub Actions cannot run the whole release procedure.
        # Releases are initiated by running a script on developer machine, which then triggers this workflow via REST API.
        print_lines(f'''\
            # Generated by scripts/configure.py
            name: release
            on: workflow_dispatch
            jobs:
              release:
                uses: robertvazan/rvscaffold/.github/workflows/net-release.yml@master
                with:
                  dotnet-version: {self.test_framework()}
                secrets:
                  nuget-token: ${{{{ secrets.NUGET_TOKEN }}}}
        ''')

    def generate_files(self):
        super().generate_files()
        if self.is_opensource():
            self.print_to(self.workflows_directory()/'build.yml', self.print_build_workflow)
        if self.nuget_release():
            self.print_to(self.workflows_directory()/'release.yml', self.print_release_workflow)
        self.print_to(self.project_path()/f'{self.root_namespace()}.csproj', self.print_csproj)
        if self.has_tests():
            self.print_to(self.test_path()/f'{self.root_namespace()}.Tests.csproj', self.print_test_csproj)
        self.print_to(f'{self.root_namespace()}.sln', self.print_sln)
        self.remove_obsolete(self.workflows_directory()/'nuget-release.yml')
        self.remove_obsolete(self.project_path()/'AssemblyInfo.cs')

class Fvc(Net):
    # def benchmark_name(self): pass
    # def benchmark_abbreviation(self): pass
    # def benchmark_url(self): pass

    def is_extractor_part(self): return False
    def is_matcher_part(self): return False
    def is_multipart_submission(self): return self.is_extractor_part() or self.is_matcher_part()
    def bundled_sister_projects(self): return []
    def has_submission_zip(self): return not self.is_multipart_submission() or self.bundled_sister_projects()
    def submission_zip(self): return f'sourceafis-fvc-{self.benchmark_abbreviation().lower()}.zip'

    def subdomain(self): return 'sourceafis'
    def homepage(self): return self.website() + 'fvc'
    def is_library(self): return False
    def assembly_name(self): return 'enroll' if self.is_extractor_part() else 'match'
    def namespace_suffix(self): return '.Extractor' if self.is_extractor_part() else '.Matcher' if self.is_matcher_part() else ''
    def root_namespace(self): return f'SourceAFIS.FVC.{self.benchmark_abbreviation()}{self.namespace_suffix()}'
    def name_suffix(self): return ' extractor' if self.is_extractor_part() else ' matcher' if self.is_matcher_part() else ''
    def pretty_name(self): return f'SourceAFIS{self.name_suffix()} for FVC {self.benchmark_abbreviation()}'
    def md_description(self): return f'''\
        Submission of [SourceAFIS](https://sourceafis.machinezoo.com/){self.name_suffix()}
        to [{self.benchmark_name()}]({self.benchmark_url()}) benchmark
        in [FVC-onGoing](https://biolab.csr.unibo.it/FVCOnGoing/UI/Form/Home.aspx) competition.

        More on [homepage]({self.homepage()}).
    '''

    def documentation_links(self):
        yield from super().documentation_links()
        yield 'SourceAFIS overview', 'https://sourceafis.machinezoo.com/'
        yield f'FVC-onGoing {self.benchmark_abbreviation()} benchmark', self.benchmark_url()

    def dependencies(self):
        yield from super().dependencies()
        yield self.use('SourceAFIS:3.14.0')

    def print_publish_script(self):
        print('#/bin/sh -e')
        print('# Generated by scripts/configure.py')
        print('cd `dirname $0`/..')
        print('dotnet publish -c release -r win-x86')
        if self.has_submission_zip():
            print(f'rm -rf {self.root_namespace()}/bin/{{submission,{self.submission_zip()}}}')
            print(f'mkdir -p {self.root_namespace()}/bin/submission')
            for project in self.bundled_sister_projects():
                print(f'cp ../{project}/*/bin/Release/net*/win-x86/publish/* {self.root_namespace()}/bin/submission/')
            print(f'cp */bin/Release/net*/win-x86/publish/* {self.root_namespace()}/bin/submission/')
            print(f'cd {self.root_namespace()}/bin/submission')
            print(f'zip ../{self.submission_zip()} *')

    def generate_files(self):
        super().generate_files()
        ps = self.path()/'scripts'/'publish.sh'
        self.print_to(ps, self.print_publish_script)
        ps.chmod(ps.stat().st_mode | 0o111)
