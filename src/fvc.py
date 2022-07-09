exec((config_directory()/'src'/'net.py').read_text())

benchmark_name = lambda: None
benchmark_abbreviation = lambda: None
benchmark_url = lambda: None
is_extractor_part = lambda: False
is_matcher_part = lambda: False

subdomain = lambda: 'sourceafis'
homepage = lambda: website() + 'fvc'
is_library = lambda: False
assembly_name = lambda: 'enroll' if is_extractor_part() else 'match'
namespace_suffix = lambda: '.Extractor' if is_extractor_part() else '.Matcher' if is_matcher_part() else ''
root_namespace = lambda: f'SourceAFIS.FVC.{benchmark_abbreviation()}{namespace_suffix()}'
name_suffix = lambda: ' extractor' if is_extractor_part() else ' matcher' if is_matcher_part() else ''
pretty_name = lambda: f'SourceAFIS{name_suffix()} for FVC {benchmark_abbreviation()}'
md_description = lambda: f'''\
	Submission of [SourceAFIS](https://sourceafis.machinezoo.com/){name_suffix()}
	to [{benchmark_name()}]({benchmark_url()}) benchmark
	in [FVC-onGoing](https://biolab.csr.unibo.it/FVCOnGoing/UI/Form/Home.aspx) competition.

	More on [homepage]({homepage()}).
'''

def documentation_links():
    yield from standard_documentation_links()
    yield 'SourceAFIS overview', 'https://sourceafis.machinezoo.com/'

def dependencies():
    use('SourceAFIS:3.14.0')
