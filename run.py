import os
from app import create_app


if __name__ == '__main__':
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    debug = config_name == 'development'
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print('\n' + '='*60)
    print('Flask Student Management System API')
    print('='*60)
    print(f'Environment: {config_name}')
    print(f'Debug Mode: {debug}')
    print(f'Server: http://localhost:{port}')
    print(f'Health Check: http://localhost:{port}/health')
    print(f'API Root: http://localhost:{port}/api')
    print('='*60 + '\n')
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
