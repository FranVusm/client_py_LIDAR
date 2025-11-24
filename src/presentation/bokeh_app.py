# src/presentation/bokeh_app.py
import datetime
from bokeh.layouts import column
from bokeh.models import MultiChoice, ColumnDataSource, Slider, Legend, LegendItem
from bokeh.plotting import figure
from bokeh.palettes import Category10

MAX_LINES = 10 

def make_bokeh_app(doc, history_repo, attrs: list):
    if not attrs:
        attrs = ["heartbeat"]

    minutes = Slider(start=1, end=60, value=10, step=1, title="Time window")

    MAX_POINTS = 1800

    multi_select = MultiChoice(
        title="Select Variables", 
        value=[attrs[0]],
        options=attrs,
        sizing_mode="stretch_width"
    )

    p = figure(
        x_axis_type="datetime",
        height=500,
        title="Sensor Data",
        sizing_mode="stretch_width",
        tools="pan,wheel_zoom,box_zoom,reset,save"
    )
    
    # --- 1. Create Pool of Sources, Lines and Points ---
    sources = []
    lines = []
    points = []  # Red points to mark each data point
    palette = Category10[MAX_LINES]
    # Mapping to track which variable is in each line
    line_to_attr = {}  # {line_index: attr_name}
    # Set to track variables hidden by user (click on legend)
    hidden_by_user = set()
    # Flag to prevent callback from interfering during update()
    updating = False

    for i in range(MAX_LINES):
        src = ColumnDataSource(data=dict(x=[], y=[]))
        
        # Create lines without legend_label (we'll handle it manually)
        line = p.line(
            'x', 'y', 
            source=src, 
            line_color=palette[i], 
            line_width=2
        )
        line.visible = False 
        
        # Create points to mark each data point (same color as line)
        point = p.scatter(
            'x', 'y',
            source=src,
            color=palette[i],  # Same color as corresponding line
            size=5,  # Size sufficient to see but not bothersome
            alpha=0.7,  # Slightly transparent to not be too prominent
            line_color=None  # No border for cleaner look
        )
        point.visible = False
        
        sources.append(src)
        lines.append(line)
        points.append(point)

    # --- 2. Configure manual legend ---
    # Create a manual legend that will be updated dynamically
    legend = Legend(
        items=[],
        location="top_left",
        click_policy="hide"
    )
    p.add_layout(legend, 'above')
    
    # Callback to track when user hides/shows lines from legend
    def on_legend_click(attr, old, new):
        # Ignore changes during update() to avoid conflicts
        if updating:
            return
        # When clicking on legend, Bokeh updates visibility
        # Track which variables are hidden and synchronize points
        for i, line in enumerate(lines):
            if i in line_to_attr:
                attr_name = line_to_attr[i]
                # Synchronize point visibility with lines
                points[i].visible = line.visible
                if not line.visible and attr_name not in hidden_by_user:
                    hidden_by_user.add(attr_name)
                elif line.visible and attr_name in hidden_by_user:
                    hidden_by_user.discard(attr_name)
    
    # Observe changes in line visibility
    for line in lines:
        line.on_change('visible', on_legend_click)

    def _decimate(xs, ys, limit):
        """Decimation that maintains temporal order"""
        n = len(xs)
        if n <= limit:
            return xs, ys
        step = max(1, n // limit)
        # Keep first and last point, and sample uniformly in the middle
        indices = [0] + list(range(step, n - 1, step)) + [n - 1]
        # Remove duplicates maintaining order
        seen = set()
        unique_indices = []
        for idx in indices:
            if idx not in seen:
                seen.add(idx)
                unique_indices.append(idx)
        return [xs[i] for i in unique_indices], [ys[i] for i in unique_indices]

    def _convert_timestamp(ts):
        """Converts datetime to timestamp in milliseconds for Bokeh"""
        # If datetime is naive (no timezone), assume UTC
        if ts.tzinfo is None:
            # naive datetime is treated as UTC
            ts = ts.replace(tzinfo=datetime.timezone.utc)
        return int(ts.timestamp() * 1000)

    def update():
        nonlocal updating
        try:
            updating = True  # Disable callbacks during update
            
            history_repo.set_retention(minutes.value)
            selected_attrs = multi_select.value
            
            # Keep only hidden variables that are still selected
            # (if a variable is deselected, it doesn't need to be in hidden_by_user)
            hidden_by_user.intersection_update(set(selected_attrs))
            
            # Clear previous mapping
            line_to_attr.clear()
            
            # List for legend items
            legend_items = []
            
            # Update lines with selected variables
            for i, attr_name in enumerate(selected_attrs):
                if i >= MAX_LINES:
                    break
                
                data = history_repo.get_history(attr_name)
                
                # Sort by timestamp to ensure chronological order
                data = sorted(data, key=lambda x: x[0])
    
                # Convert timestamps and values, maintaining order
                xs = [_convert_timestamp(ts) for ts, _ in data]
                ys = [val for _, val in data]
                
                # Decimate maintaining temporal order
                xs, ys = _decimate(xs, ys, MAX_POINTS)
    
                # Update source data
                sources[i].data = dict(x=xs, y=ys)
                
                # Register mapping before changing visibility
                line_to_attr[i] = attr_name
                
                # Make line and points visible only if not hidden by user
                if attr_name not in hidden_by_user:
                    lines[i].visible = True
                    points[i].visible = True
                else:
                    lines[i].visible = False
                    points[i].visible = False
                
                # Add item to legend (only for visible lines or that should be visible)
                legend_items.append(
                    LegendItem(
                        label=attr_name,
                        renderers=[lines[i]]
                    )
                )
    
            # Hide and clean unused lines and points
            for i in range(len(selected_attrs), MAX_LINES):
                sources[i].data = dict(x=[], y=[])
                lines[i].visible = False
                points[i].visible = False
                if i in line_to_attr:
                    del line_to_attr[i]
            
            # Update legend with new items
            legend.items = legend_items
    
            # Update title
            if selected_attrs:
                p.title.text = f"Sensor Data ({', '.join(selected_attrs)})"
            else:
                p.title.text = "Sensor Data"
    
        except Exception as e:
            print(f"[bokeh update] {e}")
        finally:
            updating = False  # Re-enable callbacks


    # --- Layout unchanged ---
    layout = column(
        multi_select, 
        p,
        minutes,
        sizing_mode="stretch_width"
    )

    doc.add_root(layout)
    doc.add_periodic_callback(update, 1000)