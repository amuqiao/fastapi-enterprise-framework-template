#!/usr/bin/env python3
"""
批量构建GraphRAG索引脚本

功能：
1. 遍历指定目录下的所有文件
2. 为每个文件创建独立的索引目录
3. 复制配置文件到索引目录
4. 准备输入数据
5. 执行构建索引命令
6. 记录构建结果

使用方法：
python batch_build_index.py --input-dir /path/to/input/files --config-dir /path/to/config/templates --output-base /path/to/output
"""

import os
import argparse
import shutil
import subprocess
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('batch_build_index.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='批量构建GraphRAG索引脚本')
    parser.add_argument('--input-dir', '-i', required=True, help='输入文件目录')
    parser.add_argument('--config-dir', '-c', required=True, help='配置文件模板目录，包含.env和settings.yaml')
    parser.add_argument('--output-base', '-o', default='./output', help='输出基础目录')
    parser.add_argument('--file-pattern', '-p', default='*.txt', help='文件匹配模式')
    parser.add_argument('--model', '-m', default=None, help='指定LLM模型，如不指定则使用配置文件中的模型')
    parser.add_argument('--embedding-model', default=None, help='指定Embedding模型，如不指定则使用配置文件中的模型')
    return parser.parse_args()

def create_index_dir(output_base, file_name):
    """为每个文件创建索引目录"""
    # 创建输出基础目录（如果不存在）
    os.makedirs(output_base, exist_ok=True)
    
    # 创建文件对应的索引目录
    index_dir = os.path.join(output_base, os.path.splitext(file_name)[0])
    os.makedirs(index_dir, exist_ok=True)
    
    # 创建input子目录
    input_dir = os.path.join(index_dir, 'input')
    os.makedirs(input_dir, exist_ok=True)
    
    return index_dir

def copy_config_files(config_dir, index_dir):
    """复制配置文件到索引目录"""
    # 复制.env文件
    env_src = os.path.join(config_dir, '.env')
    env_dest = os.path.join(index_dir, '.env')
    if os.path.exists(env_src):
        shutil.copy(env_src, env_dest)
        logger.info(f'复制.env文件到 {index_dir}')
    else:
        logger.error(f'配置目录中未找到.env文件: {env_src}')
        return False
    
    # 复制settings.yaml文件
    settings_src = os.path.join(config_dir, 'settings.yaml')
    settings_dest = os.path.join(index_dir, 'settings.yaml')
    if os.path.exists(settings_src):
        shutil.copy(settings_src, settings_dest)
        logger.info(f'复制settings.yaml文件到 {index_dir}')
    else:
        logger.error(f'配置目录中未找到settings.yaml文件: {settings_src}')
        return False
    
    # 复制prompts目录
    prompts_src = os.path.join(config_dir, 'prompts')
    prompts_dest = os.path.join(index_dir, 'prompts')
    if os.path.exists(prompts_src) and os.path.isdir(prompts_src):
        if os.path.exists(prompts_dest):
            shutil.rmtree(prompts_dest)
        shutil.copytree(prompts_src, prompts_dest)
        logger.info(f'复制prompts目录到 {index_dir}')
    else:
        logger.error(f'配置目录中未找到prompts目录: {prompts_src}')
        return False
    
    return True

def prepare_input_data(input_file, index_dir):
    """准备输入数据"""
    input_dir = os.path.join(index_dir, 'input')
    # 复制文件到input目录
    dest_file = os.path.join(input_dir, os.path.basename(input_file))
    shutil.copy(input_file, dest_file)
    logger.info(f'复制输入文件到 {dest_file}')
    return True

def build_index(index_dir):
    """执行构建索引命令"""
    logger.info(f'开始构建索引: {index_dir}')
    
    # 构建命令
    cmd = ['graphrag', 'index', '--root', index_dir]
    
    try:
        # 执行命令
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        logger.info(f'索引构建成功: {index_dir}')
        logger.debug(f'命令输出: {result.stdout}')
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f'索引构建失败: {index_dir}')
        logger.error(f'命令错误: {e.stderr}')
        return False
    except Exception as e:
        logger.error(f'执行命令时发生未知错误: {index_dir}')
        logger.error(f'错误信息: {str(e)}')
        return False

def update_config_file(index_dir, model=None, embedding_model=None):
    """更新配置文件中的模型设置"""
    if not model and not embedding_model:
        return True
    
    settings_file = os.path.join(index_dir, 'settings.yaml')
    if not os.path.exists(settings_file):
        logger.error(f'配置文件不存在: {settings_file}')
        return False
    
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新LLM模型
        if model:
            content = content.replace(
                '  model: qwen-flash',
                f'  model: {model}'
            )
        
        # 更新Embedding模型
        if embedding_model:
            content = content.replace(
                '    model: text-embedding-v2',
                f'    model: {embedding_model}'
            )
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f'更新配置文件: {settings_file}')
        return True
    except Exception as e:
        logger.error(f'更新配置文件失败: {settings_file}')
        logger.error(f'错误信息: {str(e)}')
        return False

def main():
    """主函数"""
    args = parse_args()
    
    logger.info(f'批量构建索引开始')
    logger.info(f'输入目录: {args.input_dir}')
    logger.info(f'配置目录: {args.config_dir}')
    logger.info(f'输出基础目录: {args.output_base}')
    logger.info(f'文件匹配模式: {args.file_pattern}')
    
    # 获取输入目录下的所有匹配文件
    import glob
    input_files = glob.glob(os.path.join(args.input_dir, args.file_pattern))
    
    if not input_files:
        logger.warning(f'未找到匹配的文件: {os.path.join(args.input_dir, args.file_pattern)}')
        return
    
    logger.info(f'找到 {len(input_files)} 个文件，开始批量构建索引')
    
    # 统计结果
    success_count = 0
    failure_count = 0
    failed_files = []
    
    # 遍历文件，构建索引
    for input_file in input_files:
        file_name = os.path.basename(input_file)
        logger.info(f'处理文件: {file_name}')
        
        # 创建索引目录
        index_dir = create_index_dir(args.output_base, file_name)
        
        # 复制配置文件
        if not copy_config_files(args.config_dir, index_dir):
            failure_count += 1
            failed_files.append(file_name)
            continue
        
        # 更新配置文件（如果需要）
        if not update_config_file(index_dir, args.model, args.embedding_model):
            failure_count += 1
            failed_files.append(file_name)
            continue
        
        # 准备输入数据
        if not prepare_input_data(input_file, index_dir):
            failure_count += 1
            failed_files.append(file_name)
            continue
        
        # 构建索引
        if build_index(index_dir):
            success_count += 1
        else:
            failure_count += 1
            failed_files.append(file_name)
        
        logger.info(f'完成处理文件: {file_name}\n')
    
    # 输出统计结果
    logger.info(f'批量构建索引完成')
    logger.info(f'成功: {success_count} 个文件')
    logger.info(f'失败: {failure_count} 个文件')
    if failed_files:
        logger.info(f'失败文件列表: {failed_files}')

if __name__ == '__main__':
    main()
