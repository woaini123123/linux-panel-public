a
    ��=fZ  �                   @   sh  d dl Z d dlZd dlZd dlZd dlZd dlZd dlZd dlZd dlZe j	d  dkrhe
e � e �d� e j�e�� d � d dlZd dlZd ad ad adae�� d ae�� d aej�e�� d �s�e�de��  d � ej�t�s�e�d	t � d
d� Zdd� Zedd� �Zd@dd�Zdd� Zdd� Zdd� Zdd� Z dd� Z!dd� Z"dAd d!�Z#d"d#� Z$d$d%� Z%d&d'� Z&d(d)� Z'd*d+� Z(d,d-� Z)d.d/� Z*d0d1� Z+d2d3� Z,d4d5� Z-d6d7� Z.d8d9� Z/d:d;� Z0d<d=� Z1e2d>k�rdej3e(d?�Z4e1e4�Z4e4�5�  ej3e)d?�Z6e1e6�Z6e6�5�  ej3e&d?�Z7e1e7�Z7e7�5�  ej3e/d?�Z8e1e8�Z8e8�5�  ej3e0d?�Z9e1e9�Z9e9�5�  e!�  dS )B�    N�   �utf-8z/class/corez/tmp/panelExec.logz/tmp/panelTask.plz/tmpz	mkdir -p ztouch c                 C   sT   d}t j�|�r$t|d |  � d S t�� d }t j�|�rPt|d |  � d S d S )Nz/etc/init.d/mw� z/scripts/init.d/mw)�os�path�exists�	execShell�mw�	getRunDir)�method�cmd� r   � /www/server/mdserver-web/task.py�service_cmd:   s    r   c                    s   � fdd�}|S )Nc                     s   t j� | |d�}|��  d S )N)�target�args�kwargs)�	threading�Thread�start)r   r   Zthr��fr   r   �wrapperG   s    zmw_async.<locals>.wrapperr   )r   r   r   r   r   �mw_asyncF   s    r   c                  C   s$   t �d� t�� d } t�| � d S )N�   z/scripts/init.d/mw reload &)�time�sleepr	   r
   r   )r   r   r   r   �	restartMwM   s    
r   Tc              
   C   s�   z�dd l }dd l}dd l}|r4|j�� |j|d� }| d t d }|j|||j|dd�}	|	�� d u rrt	�
d� qZ|	�� }
t|
d t�r�t|
d dd	�}t|
d
 t�r�t|
d
 dd	�}||fW S  ty� } zW Y d }~dS d }~0 0 d S )Nr   )Zsecondsz > z 2>&1i   )�cwd�stdin�shell�bufsizeg�������?r   ��encodingr   )NN)�shlex�datetime�
subprocess�now�	timedelta�logPath�Popen�PIPEZpollr   r   Zcommunicate�
isinstance�bytes�str�	Exception)Z	cmdstringr   �timeoutr    r$   r%   r&   Zend_timer   �sub�data�t1�t2�er   r   r   r   T   s(    �
r   c              
   C   s�   zpdd l }dd l}|�d� d}|j�� }|g|_|j�|� |jj| |td� t	�
� sft�d| � td� W n0 ty� } ztt|�� W Y d }~n
d }~0 0 d S )Nr   �,  )z
User-AgentzlMozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36)�filenameZ
reporthookzchown www.www Zdone)�urllib�socketZsetdefaulttimeoutZrequestZbuild_openerZ
addheadersZinstall_openerZurlretrieve�downloadHookr	   ZisAppleSystemr   �system�	writeLogsr/   r.   )�urlr7   r8   r9   �headers�openerr5   r   r   r   �downloadFilep   s     

�r@   c                 C   sF   | | }t d| | �}td| kr(d S |||d�}tt�|�� d S )Ng      Y@�d   )�total�used�pre)�intrD   r<   �json�dumps)�countZ	blockSizeZ	totalSizerC   Zpre1Zspeedr   r   r   r:   �   s    r:   c                 C   s2   z t td�}|�| � |��  W n   Y n0 d S )Nzw+)�openr)   �write�close)ZlogMsg�fpr   r   r   r<   �   s    

r<   c               
   C   s�  �z\t j�t��r\t�� } | �d��dd��dd� | �d��dd��	d��
d��� }t|� |D ]�}tt�� �}| �d��d	|d
 f��� s�qb| �d��d	|d
 f��dd|f� |d dkr�|d �d�}t|d |d � n|d dkr�t|d � tt�� �}| �d��d	|d
 f��dd|f� | �d��dd��� dk rbt �dt � qb| ��  W n2 t�y� } ztt|�� W Y d }~n
d }~0 0 t�  d S )NZtaskszstatus=?)�-1�status�0)rO   zid,type,execstrzid asc�id=?�idzstatus,startrM   �typeZdownloadZexecstrz|mw|r   r   Z	execshellz
status,end�1�rm -f )r   r   r   �isTask�db�Sql�table�whereZsetField�field�order�select�printrE   r   rH   Zsave�splitr@   r   r;   rK   r/   r.   �	siteEdate)�sqlZtaskArr�valuer   �argv�endr5   r   r   r   �runTask�   sH    
������"rd   c               
   C   s`   z&t d� t�  t d� t�d� q
W n4 tyZ }  zt�d� t�  W Y d } ~ n
d } ~ 0 0 d S )Nz
start Taskzrun wtart Taskr   �<   )r]   rd   r   r   r/   �	startTask)r5   r   r   r   rf   �   s    
rf   c               
   C   s�   z�t st�d�a t sda t�dt�� �} t | kr6W dS t�d��dd| ddf��d	��	� }d
d l
}|D ]}|�
� �|d |d � qf| a t�d| � W n0 ty� } ztt|�� W Y d }~n
d }~0 0 d S )Nzdata/edate.plz
0000-00-00z%Y-%m-%dF�sitesz.edate>? AND edate<? AND (status=? OR status=?)r   u   正在运行�id,namer   rQ   �name)�oldEdater	   �readFiler   �strftime�	localtime�MrY   rZ   r\   �site_api�stop�	writeFiler/   r]   r.   )ZmEdateZ
edateSitesro   �siter5   r   r   r   r_   �   s(    

��r_   � c                 C   s4   ddiddd�}|r||d< t j| fi |��}|jS )NzContent-Typez!application/x-www-form-urlencodedFi'  )r>   Zverifyr0   r2   )�requestsZpost�text)r=   r2   ZoptionsZresponser   r   r   �http_request2�   s    ��rv   c                 C   s   d}d| i}t ||d�S )Nzhttp://23.224.167.202:8083/�host)r2   )rv   )rw   r=   r2   r   r   r   �
http_check�   s    rx   c                  C   s�   t j �� �� } | jdkr8| jdkr8| jdkr8td� d S t j �t j�	� t �� �t j
dd� }|t j ��  �� }td� t�|� td� d S )Nr   zIt's already midnight!r   )ZdayszSleeping until midnight...zWoke up at midnight!)r%   r'   r   ZhourZminute�secondr]   Zcombine�dateZtodayr(   Ztotal_secondsr   )Zcurrent_timeZmidnightZtime_until_midnightr   r   r   �sleep_until_midnight�   s    $
r{   c                   C   s   t �  t�  d S )N)r{   �speed_check_taskr   r   r   r   �speed_check_task_daily  s    r}   c                  C   s  t �� �d�} t�d�}|�d�}|D ]}| �|d� q&t�d��d��	� }|D �]�}t�d��d��
d	|d
 f��	� }|D �]�}t�t�dd�� |�d�}td|� �� t�t|��}	g }
d}|	d d D ]\}|d dk�rd|d   kr�dk �rn n|d7 }|
�|d |d |d |d d�� q�|t|
� d }| �d��d
��
d|d
 f��	� }|�r�|d d
 }| �d��
d|f��|tt�� �d�� n$| �d��d |d
 |tt�� �f�}| �d!��
d"|f���  |
D ]2}| �d!��d#||d |d$ |d% |d f� �q�q|qPd S )&Nr;   �data/sql/system.sql�;r   rg   z,id,name,path,status,ps,addtime,edate,type_id�domainrh   zpid=?rQ   �   �   ri   zcheck domain speed: r   r2   Zall_datarR   Zsuccess��   Z	http_coder6   r   Zall_time�ip)ri   �code�
speed_timer�   rA   Zdomain_speedzdomain_id=?rP   )�success_rate�addtimez domain_id, success_rate, addtimeZdomain_speed_detailzdomain_speed_id=?z+domain_speed_id, name, code, speed_time, ipr�   r�   )rV   rW   �dbfiler	   rk   r^   �executern   rZ   r\   rY   r   r   �randomZuniform�getr]   rF   �loadsrx   �append�lenrX   �updaterE   �add�delete)r`   �csql�	csql_listZ	csql_itemrg   rr   Zdomainsr�   ri   �resultZdetailsZsuccess_countr2   r�   Zfind_domainsZdomain_speed_idZdetailr   r   r   r|     sH    


"

,�
"
�
$r|   c            "   
   C   s�  �zvdd l } dd l}| � � }d}t�� �d�}t�d�}|�d�}tt	|��D ]}|�
|| d� qNi  }}	|�� }
d }}d}d  } } } } } }}tj�|�s�t�d� q�d}z(tt�|��}|d	k r�t�d� W q�W n   d}Y n0 i }|jd	d
�|d< |d dk�rdt�d�}t�� }t�� }|d | d | d t|d � d }t�|dd� |�sz|�� |d< |}|d |d k �r�|�� |d< |}|�� }|�s�|d }|d	 }i }|d |d< |d	 |d< tt|d | d �d�|d< tt|d	 | d �d�|d< |d |d< |d |d< |d }|d	 }|�sD|}|d |d  |d |d  k�rj|}|�� }|�s||}i }|j|j |d< |j|j |d< |j|j |d < |j |j  |d!< |j!|j! |d"< |j"|j" |d#< |�s�|}nx|d  |d 7  < |d  |d 7  < |d   |d  7  < |d!  |d! 7  < |d"  |d" 7  < |d#  |d# 7  < |}|d$k�r`�z�tt�� �}||d%  }|d |d |f}|�#d&��$d'|� |�#d&��%d(|f��&�  |d d) |d d) |d |d |d |d |f}|�#d*��$d+|� |�#d*��%d(|f��&�  |d |d |d  |d! |d" |d# |f}|�#d,��$d-|� |�#d,��%d(|f��&�  |�'� }t|d. |d/  d0 d�} | d0k�r�d0} |�#d1��$d2| |d. |d3 |d4 |f� d } d }d }d }d }d}|d	7 }|d5k�rd}t�(d6d7t|� � t)�  W nB t*�y^ }! z(t+t|!�� t�(d6t|!�� W Y d }!~!n
d }!~!0 0 ~t�d)� |d	7 }q�W nX t*�y� }! z>t+t|!�� t�(d6t|!�� t)�  t�d� t,�  W Y d }!~!n
d }!~!0 0 d S )8Nr   zdata/control.confr;   r~   r   r   �
   �   r   )�intervalrC   �P   �titleu   |节点[�:u   ]处于高负载[u   ],请排查原因!u   面板监控iX  ZmemZupTotalZ	downTotali   r   ZupZdownr�   ZdownPacketsZ	upPackets�
read_count�write_count�
read_bytes�write_bytes�	read_time�
write_time�   �Q Zcpuiozpro,mem,addtimez	addtime<?r�   Znetworkz;up,down,total_up,total_down,down_packets,up_packets,addtimeZdiskiozJread_count,write_count,read_bytes,write_bytes,read_time,write_time,addtimeZone�maxrA   �load_averagezpro,one,five,fifteen,addtimeZfiveZfifteeni�  zlogs/sys_interrupt.plzreload num:)-�
system_api�psutilrV   rW   r�   r	   rk   r^   �ranger�   r�   �	cpu_countr   r   r   r   r   rE   Zcpu_percentZ	getConfigZgetHostAddrZgetDateFromNowr.   ZnotifyMessageZ
getMemUsedZpsutilNetIoCounters�round�floatZdisk_io_countersr�   r�   r�   r�   r�   r�   rX   r�   rY   r�   ZgetLoadAveragerq   r   r/   r]   �
systemTask)"r�   r�   Zsmr7   r`   r�   r�   �indexZcpuIoZcpuZcpuCountrC   rH   Z	reloadNumZ
network_upZnetwork_downZdiskio_1Zdiskio_2ZnetworkInfoZcpuInfoZdiskInfoZday�tmpZpanel_titler�   Znow_time�msgZ	networkIor�   Zdeltimer2   r�   ZlproZexr   r   r   r�   :  s&   





�
��"
��
�
���
�
��
��

�
&

r�   c                   C   sL   z*t j�t�� d �rt�  t�d� qW n   t�d� t�  Y n0 d S )Nz/data/502Task.plr�   )	r   r   r   r	   r
   �check502r   r   �check502Taskr   r   r   r   r�   �  s    
r�   c               
   C   s�   zrg d�} | D ]`}t �� }|d | d }tj�|�s8qt|�rBqt|�rtd| d � t �dd| d � qW n0 t	y� } ztt
|�� W Y d }~n
d }~0 0 d S )N)Z52Z53Z54Z55Z56Z70Z71Z72Z73Z74Z80Z81Z82Z83�/php/�/sbin/php-fpmu   检测到PHP-u   处理异常,已自动修复!u   PHP守护程序)r	   �getServerDirr   r   r   �checkPHPVersion�startPHPVersionr]   ZwriteLogr/   r.   )ZverlistZver�sdir�php_pathr5   r   r   r   r�   �  s    r�   c           	   
   C   s�  t �� }�ztt �� d |  d }tj�|�rHt �d|  � t| �rHW dS |d |  }|d |  d }tj�|�s�tj�|�r�t�|� W dS tj�|�s�W dS t�	|d	 � t| �r�W dS d
|  d }|d |  d }t �d|  d �}|d dk�rt�	d|  d � t
�d� tj�|��s.t�	d| � tj�|��sJt�	d| � t�	|d � t| ��rhW dS tj�|��r|W dS W n4 t�y� } ztt|�� W Y d }~dS d }~0 0 d S )Nz/phpz.servicezsystemctl restart phpTz/php/init.d/phpr�   r�   F� reloadz/tmp/php-cgi-z.sockz/var/run/php-fpm.pidzps -ef | grep php/z0 | grep -v grep|grep -v python |awk '{print $2}'r   rs   z> | grep -v grep|grep -v python |awk '{print $2}' | xargs kill g      �?rT   z start)r	   r�   �systemdCfgDirr   r   r   r   r�   �remover;   r   r   r/   r]   r.   )	�versionr�   Z
phpServiceZfpmr�   Zcgi�pidr2   r5   r   r   r   r�   �  sH    



r�   c                 C   s   t �� d |  d S )Nr�   z/etc/php-fpm.d/www.conf)r	   r�   )r�   r   r   r   �getFpmConfFile,  s    r�   c                 C   s�   d� | �}t| �}z�t|�}t�d|�}|s2|W S |d �d�dkrJ|W S |d �d�dkr�|d �d�}tr�|d t|d �f}q�dt|d �f}ndt|d �f}|W S    | Y S 0 d S )	Nz/tmp/php-cgi-{}.sockzlisten\s*=\s*(.+)r   �sock�����r�   r   z	127.0.0.1)	�formatr�   rk   �re�findall�findr^   ZbindrE   )r�   Zfpm_addressZphp_fpm_fileZcontentr�   Z
listen_tmpr   r   r   �getFpmAddress0  s$    
r�   c              
   C   s�   z,t | �}t�|d|  d �}t|dd�}W n( tyT } zd}W Y d }~n
d }~0 0 |�d�dkrhdS |�d�dkrzdS |�d	�dkr�dS d
S )Nz/phpfpm_status_z?jsonr   r"   zBad Gatewayr�   FzHTTP Error 404: Not FoundzConnection refusedT)r�   r	   ZrequestFcgiPHPr.   r/   r�   )r�   r�   r2   r�   r5   r   r   r   r�   G  s    r�   c               
   C   s�   ztt �� d } tj�| �s&t�d� qt �� d }d}tj�|�rLtd� ntj�|�rft�	|d � t�d� qW n: t
y� } z"tt|�� t�d� W Y d }~n
d }~0 0 d S )Nz
/openrestyr�   z/openresty.servicez/etc/init.d/openrestyzsystemctl reload openrestyr�   )r	   r�   r   r   r   r   r   r�   r   r;   r/   r]   r.   )ZodirZsystemdZinitdr5   r   r   r   �openrestyAutoRestartp  s    

r�   c                  C   s2   d} t j�| �r"t �| � td� t�d� qd S )Nzdata/restart.plZrestart_panelr   )r   r   r   r�   r   r   r   )Z
restartTipr   r   r   �restartPanelService�  s
    
r�   c                 C   s.   t jjdkr t jjdkr d| _n
| �d� | S )Nr�   r�   T)�sys�version_info�major�minor�daemon�	setDaemon)�tr   r   r   r�   �  s    
r�   �__main__)r   )NNT)rs   ):r�   r   rF   r%   r   r   r�   r�   rt   r�   �reloadZsetdefaultencodingr   r�   �getcwdr	   rV   rD   ZtimeoutCountZisCheckrj   r)   rU   r   r;   r   r   r   r   r@   r:   r<   rd   rf   r_   rv   rx   r{   r}   r|   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   �__name__r   ZsysTaskr   Zphp502Zsite_check_speed_dailyZoarZrpsr   r   r   r   �<module>   s�   


$
) !1)

