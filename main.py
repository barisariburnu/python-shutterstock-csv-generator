import os
from os.path import join


def run_public_domain_vectors():
    from spiders.publicdomainvectors import CsvGenerator

    base_path = 'PATH'
    init_num = 49

    path = join(base_path, f'{init_num}')

    while os.path.exists(path):
        generator = CsvGenerator(path, 'Signs/Symbols')
        generator.generate()

        init_num += 1
        path = join(base_path, f'{init_num}')

    print(f'[SUCCESS] Successfully completed.')
    exit(0)


def run_country_flags():
    from spiders.countryflags import CsvGenerator

    urls = CsvGenerator("T:\\Shutterstock")
    urls.generate()


if __name__ == '__main__':
    run_public_domain_vectors()
    print(f'[SUCCESS] Successfully completed.')
    exit(0)
