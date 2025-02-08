import pandas as pd
import yaml
import traceback

# Excel file constants
POSTED_COL = 'posted'
TITLE_COL = 'title'
AUTHORS_COL = 'authors'
VENUE_COL = 'venue'
YEAR_COL = 'year'
AWARD_COL = 'award (optional)'
PDF_COL = 'pdf'
SHEET_NAME = 'Papers'
EXCEL_FILE = 'C&I Papers and Blog Posts for Website.xlsx'

def normalize_string(s):
    """Normalize string for comparison by removing extra spaces and lowercasing"""
    return ' '.join(str(s).lower().split())

def papers_match(paper1, paper2):
    """Check if two papers are the same based on title and authors"""
    return (normalize_string(paper1.get('title', '')) == normalize_string(paper2.get('title', '')) and
            normalize_string(paper1.get('authors', '')) == normalize_string(paper2.get('authors', '')))

def merge_paper_info(old_paper, new_paper):
    """Merge information from two papers, updating and combining fields as needed"""
    merged = old_paper.copy()
    
    # Function to merge text fields that might have multiple values
    def merge_text_field(field):
        old_val = old_paper.get(field, '').strip()
        new_val = new_paper.get(field, '').strip()
        if not old_val:
            return new_val
        if not new_val:
            return old_val
        if normalize_string(old_val) == normalize_string(new_val):
            return old_val
        return f"{old_val}; {new_val}"

    # Merge venue information
    merged['venue'] = merge_text_field('venue')
    
    # Update/merge award information
    if 'note' in new_paper and new_paper['note']:
        if 'note' not in merged or not merged['note']:
            merged['note'] = new_paper['note']
        elif new_paper['note'] not in merged['note']:  # Avoid duplicate awards
            merged['note'] = merge_text_field('note')
    
    # Update paperurl if missing
    if 'paperurl' not in merged and 'paperurl' in new_paper:
        merged['paperurl'] = new_paper['paperurl']
    
    # Use the newer year if available
    if 'year' in new_paper:
        try:
            new_year = int(new_paper['year'])
            old_year = int(merged.get('year', 0))
            merged['year'] = max(new_year, old_year)
        except (ValueError, TypeError):
            pass
    
    return merged

def merge_paper_lists(existing_papers, new_papers):
    """Merge two lists of papers, combining duplicates"""
    merged_papers = existing_papers.copy()
    added_papers = []
    updated_papers = []
    
    for new_paper in new_papers:
        # Look for matching paper in existing list
        found_match = False
        for i, existing_paper in enumerate(merged_papers):
            if papers_match(existing_paper, new_paper):
                # Merge information and update the existing entry
                merged_papers[i] = merge_paper_info(existing_paper, new_paper)
                updated_papers.append(new_paper['title'])
                found_match = True
                break
        
        if not found_match:
            merged_papers.append(new_paper)
            added_papers.append(new_paper['title'])
    
    return merged_papers, added_papers, updated_papers



def extract_papers_from_content(content):
    # Split content into lines
    lines = content.split('\n')
    papers = []
    current_paper = []
    
    # Flag to indicate if we're currently inside a paper block
    in_paper = False
    
    for line in lines:
        # New paper starts
        if line.strip().startswith('- title:'):
            # If we were already processing a paper, save it
            if current_paper:
                papers.append('\n'.join(current_paper))
                current_paper = []
            # Start new paper
            current_paper = [line]
            in_paper = True
        # Continue current paper
        elif in_paper and line.strip() and (line.startswith('  ') or line.startswith('\t')):
            current_paper.append(line)
            
    # Don't forget to add the last paper
    if current_paper:
        papers.append('\n'.join(current_paper))
    
    return papers

def parse_existing_yml(yml_file):
    try:
        with open(yml_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract paper blocks
        paper_blocks = extract_papers_from_content(content)
        
        # Parse each block into a dictionary
        papers = []
        for block in paper_blocks:
            try:
                paper_dict = yaml.safe_load(block)
                if isinstance(paper_dict, dict):
                    papers.append(paper_dict)
                elif isinstance(paper_dict, list):
                    papers.append(paper_dict[0])
            except yaml.YAMLError as e:
                print(f"Warning: Could not parse block: {block}\nError: {e}")
                continue
                    
        return papers
    except FileNotFoundError:
        print(f"Warning: {yml_file} not found. Starting with empty list.")
        return []
    except Exception as e:
        print(f"Error parsing YAML file: {e}")
        return []

def get_excel_papers():
    try:
        # Read the Excel file and print sheet names
        excel_file = pd.ExcelFile(EXCEL_FILE)
        print("Available sheets:", excel_file.sheet_names)
        
        # Read the specific sheet
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME, skiprows=2, header=0)
        print("Available columns:", df.columns.tolist())
        
        # Filter for non-posted items
        non_posted = df[df[POSTED_COL].isna() | (df[POSTED_COL] == 0)]
        
        # Convert rows to paper dictionaries
        new_papers = []
        skipped_rows = 0
        
        for _, row in non_posted.iterrows():
            if pd.isna(row[TITLE_COL]) or not str(row[TITLE_COL]).strip():
                skipped_rows += 1
                continue
                
            paper = {
                'title': str(row[TITLE_COL]).strip(),
                'authors': str(row[AUTHORS_COL]).strip() if pd.notna(row[AUTHORS_COL]) else '',
                'venue': str(row[VENUE_COL]).strip() if pd.notna(row[VENUE_COL]) else ''
            }
            
            if pd.notna(row[YEAR_COL]):
                try:
                    paper['year'] = int(row[YEAR_COL])
                except (ValueError, TypeError):
                    paper['year'] = row[YEAR_COL]
            
            if pd.notna(row[PDF_COL]) and str(row[PDF_COL]).strip():
                paper['paperurl'] = str(row[PDF_COL]).strip()
                
            if pd.notna(row[AWARD_COL]) and str(row[AWARD_COL]).strip():
                paper['note'] = str(row[AWARD_COL]).strip()
                
            new_papers.append(paper)
            
        print(f"Processed {len(new_papers)} papers from Excel, skipped {skipped_rows} rows")
        return new_papers
        
    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred while processing Excel: {str(e)}")
        return []

def convert_and_merge_papers(existing_yml_file='../_data/publications.yml', output_file='merged_papers.md'):
    try:
        # Get existing papers from YAML
        existing_papers = parse_existing_yml(existing_yml_file)
        print(f"Found {len(existing_papers)} papers in existing YAML")
        
        # Get new papers from Excel
        new_papers = get_excel_papers()
        
        # Merge papers with duplicate detection
        all_papers, added_papers, updated_papers = merge_paper_lists(existing_papers, new_papers)
        
        # Sort by year (latest first)
        all_papers.sort(key=lambda x: x.get('year', 0), reverse=True)
        
        # Convert back to YAML format
        yml_items = []
        for paper in all_papers:
            item_lines = [f'- title: "{paper["title"]}"',
                         f'  authors: {paper["authors"]}',
                         f'  venue: {paper["venue"]}']
            
            # Add optional fields in consistent order
            if 'year' in paper:
                item_lines.append(f'  year: {paper["year"]}')
            if 'paperurl' in paper:
                item_lines.append(f'  paperurl: {paper["paperurl"]}')
            if 'note' in paper:
                item_lines.append(f'  note: {paper["note"]}')
                
            yml_items.append('\n'.join(item_lines))
        
        # Join all items with double newlines
        final_text = '\n\n'.join(yml_items)
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_text)
            
        print(f"\nSuccessfully merged and sorted {len(all_papers)} total papers:")
        print(f"- {len(existing_papers)} papers in existing YAML")
        print(f"- {len(new_papers)} papers from Excel")
        print(f"- {len(updated_papers)} papers updated with new information")
        if updated_papers:
            print("  Updated papers:")
            for title in updated_papers:
                print(f"  - {title}")
        print(f"- {len(added_papers)} new papers added")
        if added_papers:
            print("  New papers:")
            for title in added_papers:
                print(f"  - {title}")
        print(f"\nOutput written to: {output_file}")
        
    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred during merge: {str(e)}")


if __name__ == '__main__':
    convert_and_merge_papers()