import pathlib
import time
import uuid

import dash
import dash_core_components as dcc
import dash_html_components as html
from PIL import Image
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import dash_reusable_components as drc
import utils
from models.disparity_map import *

DEBUG = True
LOCAL = False
APP_PATH = str(pathlib.Path(__file__).parent.resolve())

app = dash.Dash(__name__)
server = app.server


def serve_layout():
    # Generates a session ID
    session_id = str(uuid.uuid4())

    # App Layout
    return html.Div(
        id="root",
        children=[
            # Session ID
            html.Div(session_id, id="session-id"),
            dcc.Store(id='local', storage_type='local'),
            # Main body
            html.Div(
                id="app-container",
                children=[
                    # Banner display
                    html.Div(
                        id="banner",
                        children=[
                            html.H2("Stereo Tuner", id="title"),
                        ],
                    ),
                    html.Div(
                        id="image",
                        children=[
                            # The Interactive Image Div contains the dcc Graph
                            # showing the image, as well as the hidden div storing
                            # the true image
                            html.Div(
                                id="div-interactive-image",
                                children=[
                                    utils.GRAPH_PLACEHOLDER,
                                    html.Div(
                                        id="div-storage",
                                        children=utils.STORAGE_PLACEHOLDER,
                                    ),
                                ],
                            )
                        ],
                    ),
                ],
            ),
            # Sidebar
            html.Div(
                id="sidebar",
                children=[
                    drc.Card(
                        [
                            dcc.Upload(
                                id="upload-image-left",
                                children=[
                                    "Drag and Drop or ",
                                    html.A(children="Select the Left Image"),
                                ],
                                # No CSS alternative here
                                style={
                                    "color": "darkgray",
                                    "width": "100%",
                                    "height": "8px",
                                    "lineHeight": "10px",
                                    "borderWidth": "1px",
                                    "borderStyle": "dashed",
                                    "borderRadius": "5px",
                                    "borderColor": "darkgray",
                                    "textAlign": "center",
                                    "padding": "2rem 0",
                                    "margin-bottom": "2rem",
                                },
                                accept="image/*",
                            ),
                            dcc.Upload(
                                id="upload-image-right",
                                children=[
                                    "Drag and Drop or ",
                                    html.A(children="Select the Right Image"),
                                ],
                                # No CSS alternative here
                                style={
                                    "color": "darkgray",
                                    "width": "100%",
                                    "height": "8px",
                                    "lineHeight": "10px",
                                    "borderWidth": "1px",
                                    "borderStyle": "dashed",
                                    "borderRadius": "5px",
                                    "borderColor": "darkgray",
                                    "textAlign": "center",
                                    "padding": "2rem 0",
                                    "margin-bottom": "2rem",
                                },
                                accept="image/*",
                            ),
                            drc.NamedInlineRadioItems(
                                name="Algorithm",
                                short="algo",
                                options=[
                                    {"label": " Stereo-BM", "value": "bm"},
                                    {"label": " Stereo-SGBM", "value": "sgbm"},
                                ],
                                val="bm",
                            ),
                        ]
                    ),
                    drc.Card(
                        [
                            drc.CustomSlider("Block size", min=1, max=11, step=2, value=5, allow_inter=False),
                            drc.CustomSlider("Number of disparities", min=16, max=16 * 17, step=16, value=64, allow_inter=False),
                            drc.CustomSlider("Min disparity", min=0, max=16 * 17, step=16, value=0, allow_inter=False),
                            drc.CustomSlider("P1", min=0, max=256, step=16, value=0),
                            drc.CustomSlider("P2", min=0, max=256, step=16, value=0),
                            drc.CustomSlider("Disp 12 Max Diff", min=0, max=2, step=1, value=0),
                            drc.CustomSlider("Uniqueness Ratio", min=0, max=20, step=1, value=0),
                            drc.CustomSlider("Pre Filter Cap", min=1, max=63, step=2, value=1),
                            drc.CustomSlider("Speckle Windows Size", min=0, max=256, step=16, value=0),
                            drc.CustomSlider("Speckle Range", min=0, max=256, step=16, value=0)
                        ]
                    )
                ],
            ),
        ],
    )


app.layout = serve_layout


@app.callback(
    [
        Output("val-Block size", "children"),
        Output("val-Number of disparities", "children"),
        Output("val-Min disparity", "children"),
        Output("val-P1", "children"),
        Output("val-P2", "children"),
        Output("val-Disp 12 Max Diff", "children"),
        Output("val-Uniqueness Ratio", "children"),
        Output("val-Pre Filter Cap", "children"),
        Output("val-Speckle Windows Size", "children"),
        Output("val-Speckle Range", "children")
    ]
    ,
    [
        Input("slider-Block size", "value"),
        Input("slider-Number of disparities", "value"),
        Input("slider-Min disparity", "value"),
        Input("slider-P1", "value"),
        Input("slider-P2", "value"),
        Input("slider-Disp 12 Max Diff", "value"),
        Input("slider-Uniqueness Ratio", "value"),
        Input("slider-Pre Filter Cap", "value"),
        Input("slider-Speckle Windows Size", "value"),
        Input("slider-Speckle Range", "value")
    ]
)
def update_param_display(block_size,
                         n_disparities,
                         min_disparities,
                         p1,
                         p2,
                         disp_12_max_diff,
                         uniqueness_ratio,
                         pre_filter_cap,
                         speckle_windows_size,
                         speckle_range):
    return f"Block size: {block_size}", \
           f"Number of disparities: {n_disparities}", \
           f"Min number of disparities: {min_disparities}", f"P1: {p1}", f"P2: {p2}", \
           f"Disp 12 Max Diff: {disp_12_max_diff}", f"Uniqueness ratio: {uniqueness_ratio}", \
           f"Pre Filter Cap: {pre_filter_cap}", f"Speckle Windows Size: {speckle_windows_size}", \
           f"Speckle Range: {speckle_range}"


@app.callback(
    [
        Output("div-interactive-image", "children"),
        Output("local", "data")
    ]
    ,
    [
        Input("upload-image-left", "contents"),
        Input("upload-image-right", "contents"),
        Input("radio-algo", "value"),
        Input("slider-Block size", "value"),
        Input("slider-Number of disparities", "value"),
        Input("slider-Min disparity", "value"),
        Input("slider-P1", "value"),
        Input("slider-P2", "value"),
        Input("slider-Disp 12 Max Diff", "value"),
        Input("slider-Uniqueness Ratio", "value"),
        Input("slider-Pre Filter Cap", "value"),
        Input("slider-Speckle Windows Size", "value"),
        Input("slider-Speckle Range", "value")
    ],
    [
        State("upload-image-left", "filename"),
        State("upload-image-right", "filename"),
        State("local", "data")
    ],
)
def update_graph_interactive_image(
        left_content,
        right_content,
        # sliders
        algo,
        block_size,
        n_disparities,
        min_disparities,
        p1,
        p2,
        disp_12_max_diff,
        uniqueness_ratio,
        pre_filter_cap,
        speckle_windows_size,
        speckle_range,
        # states
        new_left_name,
        new_right_name,
        data
):
    t_start = time.time()
    data = data or {'left': {'filename': None, 'image': None}, 'right': {'filename': None, 'image': None}}

    left_name = data['left']['filename']
    right_name = data['right']['filename']

    # If a new file was uploaded (new file name changed) update the local storage
    if new_left_name and new_left_name != left_name:
        data['left']['filename'] = new_left_name
        data['left']['image'] = left_content.split(";base64,")[-1]
    if new_right_name and new_right_name != right_name:
        data['right']['filename'] = new_right_name
        data['right']['image'] = right_content.split(";base64,")[-1]

    if data['left']['image'] is not None and data['right']['image'] is not None:
        # convert to images
        left = drc.b64_to_numpy(data['left']['image'], to_scalar=False)
        right = drc.b64_to_numpy(data['right']['image'], to_scalar=False)


        if algo == "bm":
            disparity_map = generate_stereo_bm_disparity_map(left, right,
                                                             min_disp=min_disparities,
                                                             num_disp=n_disparities,
                                                             block_size=block_size,
                                                             prefilter_cap=pre_filter_cap,
                                                             disp12maxdiff=disp_12_max_diff,
                                                             uniqueness_ratio=uniqueness_ratio,
                                                             speckle_windows_size=speckle_windows_size,
                                                             speckle_range=speckle_range)
        else:
            disparity_map = generate_stereo_sgbm_disparity_map(left, right,
                                                               min_disp=min_disparities,
                                                               num_disp=n_disparities,
                                                               block_size=block_size,
                                                               p1=p1,
                                                               p2=p2,
                                                               prefilter_cap=pre_filter_cap,
                                                               disp12maxdiff=disp_12_max_diff,
                                                               uniqueness_ratio=uniqueness_ratio,
                                                               speckle_windows_size=speckle_windows_size,
                                                               speckle_range=speckle_range)
        disparity_map = cv2.normalize(disparity_map, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX,
                                      dtype=cv2.CV_8U)
        result = Image.fromarray(disparity_map)
    else:
        raise PreventUpdate

    t_end = time.time()
    if DEBUG:
        print(f"Image processed on {t_end - t_start:.3f} sec")

    return [
               drc.InteractiveImagePIL(
                   image_id="interactive-image",
                   image=result,
                   enc_format="png",
                   dragmode="select",
                   verbose=DEBUG,
               )
           ], data


# Running the server
if __name__ == "__main__":
    app.run_server(debug=False)
