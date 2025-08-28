import re
import json
from typing import List, Dict, Any
from jinja2 import Environment, FileSystemLoader, Template
from models import GeneratedFile, AppMetadata

class CodeGenerator:
    """Main code generator class for creating app starter code"""
    
    def __init__(self):
        """Initialize Jinja2 environment for template rendering"""
        self.env = Environment(
            loader=FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Common app type patterns
        self.app_patterns = {
            'todo': ['todo', 'task', 'checklist', 'reminder'],
            'blog': ['blog', 'post', 'article', 'cms'],
            'ecommerce': ['shop', 'store', 'ecommerce', 'product', 'cart'],
            'social': ['social', 'chat', 'message', 'friend'],
            'dashboard': ['dashboard', 'analytics', 'chart', 'report'],
            'portfolio': ['portfolio', 'showcase', 'gallery'],
            'calculator': ['calculator', 'compute', 'math'],
            'weather': ['weather', 'forecast', 'climate'],
            'note': ['note', 'notebook', 'memo', 'journal']
        }
    
    def analyze_app_idea(self, idea: str) -> AppMetadata:
        """
        Analyze the app idea to extract metadata for code generation
        
        Args:
            idea: User's app idea description
            
        Returns:
            AppMetadata object with extracted information
        """
        idea_lower = idea.lower()
        
        # Determine app type
        app_type = 'generic'
        for type_name, keywords in self.app_patterns.items():
            if any(keyword in idea_lower for keyword in keywords):
                app_type = type_name
                break
        
        # Generate app name from idea
        app_name = self._generate_app_name(idea)
        
        # Determine frontend complexity
        frontend_type = 'html'  # Default to simple HTML
        if any(word in idea_lower for word in ['complex', 'interactive', 'dynamic', 'real-time']):
            frontend_type = 'react'
        elif app_type in ['todo', 'blog', 'ecommerce', 'social', 'dashboard']:
            frontend_type = 'react'
        
        # Extract features
        features = self._extract_features(idea_lower, app_type)
        
        # Determine if database is needed
        database_needed = any(word in idea_lower for word in [
            'save', 'store', 'database', 'persist', 'user', 'account', 'login'
        ]) or app_type in ['todo', 'blog', 'ecommerce', 'social']
        
        # Generate API endpoints
        api_endpoints = self._generate_api_endpoints(app_type, features)
        
        return AppMetadata(
            app_name=app_name,
            app_type=app_type,
            frontend_type=frontend_type,
            features=features,
            database_needed=database_needed,
            api_endpoints=api_endpoints
        )
    
    def generate_app_code(self, idea: str) -> List[GeneratedFile]:
        """
        Generate complete app code based on the idea
        
        Args:
            idea: User's app idea description
            
        Returns:
            List of GeneratedFile objects
        """
        metadata = self.analyze_app_idea(idea)
        files = []
        
        # Generate backend files
        files.extend(self._generate_backend_files(metadata))
        
        # Generate frontend files
        files.extend(self._generate_frontend_files(metadata))
        
        # Generate README
        files.append(self._generate_readme(metadata, idea))
        
        return files
    
    def _generate_app_name(self, idea: str) -> str:
        """Extract or generate app name from idea"""
        # Try to extract app name from phrases like "a todo app" or "todo list app"
        words = re.findall(r'\b\w+\b', idea.lower())
        
        # Look for app type keywords
        app_keywords = []
        for type_name, keywords in self.app_patterns.items():
            if any(keyword in words for keyword in keywords):
                app_keywords.extend([kw for kw in keywords if kw in words])
                break
        
        if app_keywords:
            return f"{app_keywords[0]}_app"
        elif len(words) >= 2:
            return f"{words[0]}_{words[1]}_app"
        else:
            return "my_app"
    
    def _extract_features(self, idea_lower: str, app_type: str) -> List[str]:
        """Extract features from the idea"""
        features = []
        
        # Common feature patterns
        feature_patterns = {
            'authentication': ['login', 'signup', 'auth', 'user', 'account'],
            'crud': ['add', 'create', 'delete', 'edit', 'update', 'remove'],
            'search': ['search', 'find', 'filter'],
            'notifications': ['notify', 'alert', 'notification'],
            'file_upload': ['upload', 'file', 'image', 'photo'],
            'real_time': ['real-time', 'live', 'instant'],
            'comments': ['comment', 'feedback', 'review'],
            'categories': ['category', 'tag', 'group'],
            'sharing': ['share', 'export', 'send']
        }
        
        for feature, keywords in feature_patterns.items():
            if any(keyword in idea_lower for keyword in keywords):
                features.append(feature)
        
        # Add default features based on app type
        if app_type == 'todo':
            features.extend(['crud', 'categories'])
        elif app_type == 'blog':
            features.extend(['crud', 'comments', 'categories'])
        elif app_type == 'ecommerce':
            features.extend(['crud', 'search', 'categories', 'authentication'])
        
        return list(set(features))  # Remove duplicates
    
    def _generate_api_endpoints(self, app_type: str, features: List[str]) -> List[str]:
        """Generate API endpoints based on app type and features"""
        endpoints = []
        
        # Base endpoints by app type
        if app_type == 'todo':
            endpoints = ['/tasks', '/tasks/{id}']
        elif app_type == 'blog':
            endpoints = ['/posts', '/posts/{id}']
        elif app_type == 'ecommerce':
            endpoints = ['/products', '/products/{id}', '/cart']
        elif app_type == 'note':
            endpoints = ['/notes', '/notes/{id}']
        else:
            endpoints = ['/items', '/items/{id}']
        
        # Add feature-based endpoints
        if 'authentication' in features:
            endpoints.extend(['/auth/login', '/auth/register'])
        if 'search' in features:
            endpoints.append('/search')
        if 'categories' in features:
            endpoints.append('/categories')
        
        return endpoints
    
    def _generate_backend_files(self, metadata: AppMetadata) -> List[GeneratedFile]:
        """Generate backend files"""
        files = []
        
        # Generate main FastAPI file
        template = self.env.get_template('fastapi_main.j2')
        content = template.render(metadata=metadata)
        files.append(GeneratedFile(
            path="backend/main.py",
            content=content,
            file_type="python"
        ))
        
        return files
    
    def _generate_frontend_files(self, metadata: AppMetadata) -> List[GeneratedFile]:
        """Generate frontend files"""
        files = []
        
        if metadata.frontend_type == 'react':
            # Generate React App
            app_template = self.env.get_template('react_app.j2')
            app_content = app_template.render(metadata=metadata)
            files.append(GeneratedFile(
                path="frontend/src/App.js",
                content=app_content,
                file_type="javascript"
            ))
            
            # Generate main component
            component_template = self.env.get_template('react_component.j2')
            component_content = component_template.render(metadata=metadata)
            files.append(GeneratedFile(
                path=f"frontend/src/components/{metadata.app_type.title()}Component.js",
                content=component_content,
                file_type="javascript"
            ))
            
            # Generate index.html
            files.append(GeneratedFile(
                path="frontend/public/index.html",
                content=self._generate_react_index_html(metadata),
                file_type="html"
            ))
            
        else:
            # Generate simple HTML app
            html_template = self.env.get_template('html_app.j2')
            html_content = html_template.render(metadata=metadata)
            files.append(GeneratedFile(
                path="frontend/index.html",
                content=html_content,
                file_type="html"
            ))
        
        return files
    
    def _generate_readme(self, metadata: AppMetadata, original_idea: str) -> GeneratedFile:
        """Generate README.md file"""
        template = self.env.get_template('readme.j2')
        content = template.render(metadata=metadata, original_idea=original_idea)
        
        return GeneratedFile(
            path="README.md",
            content=content,
            file_type="markdown"
        )
    
    def _generate_react_index_html(self, metadata: AppMetadata) -> str:
        """Generate index.html for React app"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata.app_name.replace('_', ' ').title()}</title>
    <script src="https://unpkg.com/react@17/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@17/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel" src="src/App.js"></script>
</body>
</html>"""
