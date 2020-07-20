# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Construction of the master pipeline.
"""

from typing import Dict

from kedro.pipeline import Pipeline, node

from bnhm.nodes import generate_value_count_barh, get_basis_of_record_by_collection_code_plot, \
    get_elevation_plot, get_collection_code_map, get_reserve_data, get_reserve_map


def create_pipelines(**kwargs) -> Dict[str, Pipeline]:
    """Create the project's pipeline.

    Args:
        kwargs: Ignore any additional arguments added in the future.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.

    """

    return {
        "de": Pipeline([
            node(lambda x: x, inputs='GBIF', outputs='01_raw/gbif_species_data.csv'),
            node(get_reserve_data, inputs=None, outputs='01_raw/reserves.json')
        ]),
        "__default__": Pipeline(
            [
                node(
                    generate_value_count_barh(col),
                    inputs='01_raw/gbif_species_data.csv',
                    outputs=f'03_primary/{col}_value_plot.png'
                )
                for col in ['country', 'county', 'basisOfRecord', 'collectionCode']
            ] +
            [
                node(
                    get_basis_of_record_by_collection_code_plot,
                    inputs='01_raw/gbif_species_data.csv',
                    outputs='03_primary/basis_of_record_by_collection_code_plot.png'
                ),
                node(
                    get_elevation_plot,
                    inputs='01_raw/gbif_species_data.csv',
                    outputs='03_primary/elevation_plot.png'),
            ] +
            [
                node(
                    get_collection_code_map,
                    inputs='01_raw/gbif_species_data.csv',
                    outputs='03_primary/collection_code.html',
                ),
                node(
                    get_reserve_map,
                    inputs=['01_raw/gbif_species_data.csv', '01_raw/reserves.json'],
                    outputs='03_primary/reserve_map.html',
                )
            ]
        )
    }
